# controller/save_manager.py
import json
import os
from model.constants import DATA_DIR


SAVE_FILE = os.path.join(DATA_DIR, "save.json")


class SaveManager:
    def save(self, player, mission_manager):
        data = {
            "score":      player.score,
            "mission":    mission_manager.current,
            "completed":  list(mission_manager.completed),
        }
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        if not os.path.exists(SAVE_FILE):
            return None
        try:
            with open(SAVE_FILE) as f:
                return json.load(f)
        except Exception:
            return None

    def has_save(self):
        return os.path.exists(SAVE_FILE)
