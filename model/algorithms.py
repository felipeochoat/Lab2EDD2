# model/algorithms.py
"""
Graph algorithms for NetGuardian.
Each algorithm is a generator that yields steps so the view can
animate them frame by frame without blocking.
"""
import heapq
from collections import deque


# ── BFS ──────────────────────────────────────────────────────────────────────
def bfs(graph, start=0):
    """
    Breadth-First Search.
    Yields: ('visit', node_id) | ('queue', node_id) | ('edge', edge) | ('done', origin_id)
    """
    graph.reset_algo_state()
    queue   = deque([start])
    visited = set([start])
    graph.nodes[start].in_queue = True

    while queue:
        uid = queue.popleft()
        node = graph.nodes[uid]
        node.visited  = True
        node.in_queue = False
        yield ('visit', uid)

        if node.node_type == 'origin':
            yield ('done', uid)
            return

        for e in graph._adj[uid]:
            nid = e.other(uid)
            e.lit = 1.0
            yield ('edge', e)
            if nid not in visited:
                visited.add(nid)
                graph.nodes[nid].in_queue = True
                queue.append(nid)
                yield ('queue', nid)

    yield ('exhausted', -1)


# ── DFS ──────────────────────────────────────────────────────────────────────
def dfs(graph, start=0):
    """
    Depth-First Search (iterative).
    Yields: ('visit', node_id) | ('edge', edge) | ('done', origin_id)
    """
    graph.reset_algo_state()
    stack   = [start]
    visited = set()

    while stack:
        uid = stack.pop()
        if uid in visited:
            continue
        visited.add(uid)
        node = graph.nodes[uid]
        node.visited = True
        yield ('visit', uid)

        if node.node_type == 'origin':
            yield ('done', uid)
            return

        for e in graph._adj[uid]:
            nid = e.other(uid)
            e.lit = 0.8
            yield ('edge', e)
            if nid not in visited:
                stack.append(nid)

    yield ('exhausted', -1)


# ── DIJKSTRA ─────────────────────────────────────────────────────────────────
def dijkstra(graph, src, dst):
    """
    Dijkstra's shortest path.
    Yields: ('relax', node_id) | ('visit', node_id) | ('path', [node_ids]) | ('done', cost)
    """
    graph.reset_algo_state()
    n = len(graph.nodes)
    dist = [float('inf')] * n
    prev = [-1] * n
    dist[src] = 0
    pq = [(0, src)]

    while pq:
        d, uid = heapq.heappop(pq)
        if graph.nodes[uid].visited:
            continue
        graph.nodes[uid].visited = True
        graph.nodes[uid].dist = d
        yield ('visit', uid)

        if uid == dst:
            break

        for e in graph._adj[uid]:
            nid = e.other(uid)
            nd = d + e.weight
            if nd < dist[nid]:
                dist[nid] = nd
                prev[nid] = uid
                graph.nodes[nid].dist = nd
                heapq.heappush(pq, (nd, nid))
                e.lit = 0.7
                yield ('relax', nid)

    # Reconstruct path
    path = []
    cur  = dst
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
    path.reverse()

    for i in range(len(path) - 1):
        e = graph.edge_between(path[i], path[i+1])
        if e:
            e.in_path = True
    yield ('path', path)
    yield ('done', dist[dst] if dist[dst] != float('inf') else -1)


# ── KRUSKAL (MST) ─────────────────────────────────────────────────────────────
def kruskal(graph):
    """
    Kruskal's Minimum Spanning Tree.
    Yields: ('consider', edge) | ('accept', edge) | ('reject', edge) | ('done', total_cost)
    """
    graph.reset_algo_state()
    edges_sorted = sorted(graph.edges, key=lambda e: e.weight)
    parent = {n.id: n.id for n in graph.nodes}
    rank   = {n.id: 0    for n in graph.nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True

    total = 0
    for e in edges_sorted:
        yield ('consider', e)
        if union(e.a, e.b):
            e.in_mst = True
            graph.nodes[e.a].visited = True
            graph.nodes[e.b].visited = True
            total += e.weight
            yield ('accept', e)
        else:
            yield ('reject', e)

    yield ('done', total)


# ── FORD-FULKERSON (BFS augmenting paths) ────────────────────────────────────
def ford_fulkerson(graph, source, sink):
    """
    Ford-Fulkerson max flow using BFS (Edmonds-Karp).
    Yields: ('path', path_edges) | ('augment', flow_val) | ('done', max_flow)
    """
    graph.reset_algo_state()
    # Build residual as dict: (u,v)->capacity
    res = {}
    for e in graph.edges:
        key_fwd = (e.a, e.b)
        key_rev = (e.b, e.a)
        res[key_fwd] = res.get(key_fwd, 0) + e.capacity
        res[key_rev] = res.get(key_rev, 0)

    max_flow = 0

    def bfs_path():
        visited = {source}
        queue   = deque([(source, [])])
        while queue:
            u, path = queue.popleft()
            for (a, b), cap in res.items():
                if a == u and b not in visited and cap > 0:
                    new_path = path + [(a, b)]
                    if b == sink:
                        return new_path
                    visited.add(b)
                    queue.append((b, new_path))
        return None

    while True:
        path_edges = bfs_path()
        if not path_edges:
            break

        # Mark path edges in graph for visualisation
        path_flow = min(res[e] for e in path_edges)
        for (a, b) in path_edges:
            ge = graph.edge_between(a, b) or graph.edge_between(b, a)
            if ge:
                ge.active = True
                ge.lit    = 1.0
                ge.flow   = min(ge.flow + path_flow, ge.capacity)
        yield ('path', path_edges)

        for (a, b) in path_edges:
            res[(a, b)] -= path_flow
            res[(b, a)]  = res.get((b, a), 0) + path_flow

        max_flow += path_flow
        yield ('augment', path_flow)

    yield ('done', max_flow)
