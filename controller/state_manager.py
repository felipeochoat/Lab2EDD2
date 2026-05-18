# controller/state_manager.py


class GameState:
    MENU    = "menu"
    PLAYING = "playing"
    PAUSED  = "paused"
    VICTORY = "victory"
    CINEMATIC = "cinematic"


class StateManager:
    def __init__(self):
        self.state = GameState.MENU
        self._prev = None

    def transition(self, new_state):
        self._prev = self.state
        self.state = new_state

    def back(self):
        if self._prev:
            self.state = self._prev

    def is_playing(self):
        return self.state == GameState.PLAYING

    def is_menu(self):
        return self.state == GameState.MENU

    def is_victory(self):
        return self.state == GameState.VICTORY
