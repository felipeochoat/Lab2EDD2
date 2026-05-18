# controller/mission_manager.py
from model.emotions import MISSIONS

# Requisitos reales por misión — usan los mismos IDs que los botones del juego
MISSION_REQUIREMENTS = {
    0: {"bfs", "dfs"},        # M1: basta con uno de los dos
    1: {"dijkstra"},
    2: {"kruskal"},
    3: {"ff"},
    4: {"bfs", "dijkstra", "kruskal", "ff"},
}

# Misión 0 y 4 se completan con AL MENOS UNO de los requeridos
MISSION_ANY = {0, 4}


class MissionManager:
    """Tracks mission progress and unlocks."""

    def __init__(self):
        self.current   = 0
        self.completed = set()
        self.algo_done = {}   # mission_id -> set of algo ids done

    def complete_algo(self, mission_id, algo):
        if mission_id not in self.algo_done:
            self.algo_done[mission_id] = set()
        self.algo_done[mission_id].add(algo)

    def is_mission_complete(self, mission_id):
        req  = MISSION_REQUIREMENTS.get(mission_id, set())
        done = self.algo_done.get(mission_id, set())
        if mission_id in MISSION_ANY:
            # Complete if at least one required algo was run
            return bool(req & done)
        # Complete when ALL required algos done
        return req.issubset(done)

    def advance(self):
        if self.current < len(MISSIONS) - 1:
            self.completed.add(self.current)
            self.current += 1
            return True
        return False

    def all_done(self):
        return len(self.completed) >= len(MISSIONS) - 1

    def current_info(self):
        return MISSIONS[self.current]

    def reward(self, mission_id):
        return MISSIONS[mission_id].get('reward', 30)
