# controller/save_manager.py
import json
import os
from model.constants import DATA_DIR


SAVE_FILE       = os.path.join(DATA_DIR, "save.json")
SAVE_FILE_MULTI = os.path.join(DATA_DIR, "save_multi.json")


class SaveManager:
    def save(self, player, mission_manager, multi=False):
        path = SAVE_FILE_MULTI if multi else SAVE_FILE
        data = {
            "score":      player.score,
            "mission":    mission_manager.current,
            "completed":  list(mission_manager.completed),
        }
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self, multi=False):
        path = SAVE_FILE_MULTI if multi else SAVE_FILE
        if not os.path.exists(path):
            return None
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            return None

    def has_save(self, multi=False):
        path = SAVE_FILE_MULTI if multi else SAVE_FILE
        return os.path.exists(path)