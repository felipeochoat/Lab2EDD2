# model/graph.py
import math
import random

class Node:
    """Represents a user in the social network (graph node)."""
    def __init__(self, node_id, name, x, y, node_type="neutral"):
        self.id        = node_id
        self.name      = name
        self.x         = float(x)
        self.y         = float(y)
        self.node_type = node_type   # victim / bully / follower / ally / observer / bot / origin

        # Visual state
        self.visited    = False
        self.in_queue   = False
        self.highlighted= False
        self.pulse      = random.uniform(0, math.pi * 2)
        self.radius     = 14

        # Graph algo state
        self.dist       = float('inf')   # Dijkstra distance
        self.prev       = -1             # predecessor

        # NPC world state
        self.world_x    = 0.0
        self.world_vx   = random.choice([-0.6, 0.6])
        self.facing     = 1
        self.emotion    = "neutral"      # happy / sad / angry / neutral
        self.talked_to  = False

    def reset_algo(self):
        self.visited     = False
        self.in_queue    = False
        self.highlighted = False
        self.dist        = float('inf')
        self.prev        = -1

    def __repr__(self):
        return f"Node({self.id}, {self.name}, {self.node_type})"


class Edge:
    """Represents a social relationship (graph edge)."""
    def __init__(self, a, b, weight=1, capacity=5):
        self.a        = a          # node id
        self.b        = b          # node id
        self.weight   = weight     # emotional risk / cost
        self.capacity = capacity   # max flow capacity
        self.flow     = 0          # current flow (Ford-Fulkerson)

        # Visual state
        self.active   = False      # currently traversed
        self.in_mst   = False      # part of MST
        self.in_path  = False      # part of shortest path
        self.lit      = 0.0        # glow intensity 0-1
        self.particles= []         # travelling particles

    def reset_algo(self):
        self.active  = False
        self.in_mst  = False
        self.in_path = False
        self.lit     = 0.0
        self.flow    = 0
        self.particles = []

    def other(self, node_id):
        return self.b if self.a == node_id else self.a

    def residual_capacity(self, from_node):
        if self.a == from_node:
            return self.capacity - self.flow
        return self.flow  # reverse edge

    def __repr__(self):
        return f"Edge({self.a}-{self.b}, w={self.weight}, cap={self.capacity})"


class SocialGraph:
    """The social network graph. Adjacency list internally."""

    NPC_NAMES = [
        "ARIA","ZETA","NEXUS","VOLT","ECHO","PIXEL",
        "GHOST","NOVA","RAZE","LYRA","CYPH","APEX","FLUX","VEGA"
    ]
    NPC_TYPES = [
        "ally","observer","neutral","bully","follower",
        "ally","bot","bully","follower","victim","observer","ally","neutral","follower"
    ]

    def __init__(self, n=12, seed=42):
        random.seed(seed)
        self.nodes  = []
        self.edges  = []
        self._adj   = {}   # node_id -> list of Edge
        self._build(n)

    def _build(self, n):
        import math
        from model.constants import SCREEN_W, GRAPH_PANEL_H
        cx = SCREEN_W / 2
        cy = GRAPH_PANEL_H / 2 - 10
        r_outer = min(SCREEN_W, GRAPH_PANEL_H) * 0.36
        r_inner = r_outer * 0.40

        for i in range(n):
            angle = (i / n) * math.pi * 2 - math.pi / 2
            if i % 3 == 0:
                rx, ry = r_outer * 0.95, r_outer * 0.68
            else:
                rx, ry = r_outer * 0.88, r_outer * 0.62
            x = cx + rx * math.cos(angle)
            y = cy + ry * math.sin(angle)
            name = self.NPC_NAMES[i % len(self.NPC_NAMES)]
            ntype= self.NPC_TYPES[i % len(self.NPC_TYPES)]
            node = Node(i, name, x, y, ntype)
            self.nodes.append(node)
            self._adj[i] = []

        # Mark origin (hidden bully who started everything)
        origin_id = random.randint(3, n - 2)
        self.nodes[origin_id].node_type = "origin"
        self.nodes[origin_id].name = "???"
        self.origin_id = origin_id

        # Mark victim
        victim_id = (origin_id + n // 2) % n
        self.nodes[victim_id].node_type = "victim"
        self.victim_id = victim_id

        # Edges: ring + cross connections
        pairs = []
        for i in range(n):
            pairs.append((i, (i+1) % n))
        extras = [(0,3),(1,5),(2,7),(4,8),(6,10),(3,9),(5,11),(7,2),(9,4),(11,6),(0,6),(origin_id, victim_id)]
        for a, b in extras:
            if a < n and b < n and a != b:
                pairs.append((a, b))

        seen = set()
        for a, b in pairs:
            key = (min(a,b), max(a,b))
            if key in seen:
                continue
            seen.add(key)
            w   = random.randint(1, 9)
            cap = random.randint(2, 7)
            e = Edge(a, b, w, cap)
            self.edges.append(e)
            self._adj[a].append(e)
            self._adj[b].append(e)

    def neighbors(self, node_id):
        return [e.other(node_id) for e in self._adj[node_id]]

    def edge_between(self, a, b):
        for e in self._adj[a]:
            if e.other(a) == b:
                return e
        return None

    def reset_algo_state(self):
        for n in self.nodes:
            n.reset_algo()
        for e in self.edges:
            e.reset_algo()

    def visited_count(self):
        return sum(1 for n in self.nodes if n.visited)

    def toxicity_level(self):
        toxic_types = {"bully","follower","bot","origin"}
        toxic = sum(1 for n in self.nodes if n.node_type in toxic_types)
        return toxic / max(len(self.nodes), 1)
