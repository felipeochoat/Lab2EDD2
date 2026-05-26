# controller/sound_manager.py
"""
SoundManager — Sistema de audio procedural para NetGuardian.
Genera todos los sonidos usando numpy + pygame.sndarray.
No requiere archivos de audio externos.
"""
import math
import random
import pygame
import numpy as np

SAMPLE_RATE = 44100


# ──────────────────────────────────────────────────────────
#  GENERADORES DE ONDA BÁSICOS
# ──────────────────────────────────────────────────────────

def _sine(freq, t):
    return np.sin(2 * np.pi * freq * t)

def _square(freq, t, duty=0.5):
    phase = (t * freq) % 1.0
    return np.where(phase < duty, 1.0, -1.0).astype(np.float32)

def _sawtooth(freq, t):
    return (2 * ((t * freq) % 1.0) - 1.0).astype(np.float32)

def _noise(frames):
    return np.random.uniform(-1, 1, frames).astype(np.float32)

def _envelope(frames, attack=0.01, decay=0.1, sustain=0.7, release=0.1):
    env = np.ones(frames, dtype=np.float32)
    a = int(attack * SAMPLE_RATE)
    d = int(decay  * SAMPLE_RATE)
    r = int(release * SAMPLE_RATE)
    if a > 0: env[:a] = np.linspace(0, 1, a)
    if d > 0 and a + d < frames: env[a:a+d] = np.linspace(1, sustain, d)
    if a + d < frames - r: env[a+d:frames-r] = sustain
    if r > 0 and frames - r >= 0: env[frames-r:] = np.linspace(sustain, 0, r)
    return env

def _make_sound(arr, volume=1.0):
    arr = np.clip(arr * volume, -1, 1)
    s16 = (arr * 32767).astype(np.int16)
    stereo = np.ascontiguousarray(np.column_stack([s16, s16]))
    return pygame.sndarray.make_sound(stereo)


# ──────────────────────────────────────────────────────────
#  GENERADORES DE SONIDOS ESPECÍFICOS
# ──────────────────────────────────────────────────────────

def _gen_click(vol=0.5):
    dur = 0.07; frames = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, frames, False)
    arr = _sine(900, t) * 0.5 + _sine(1400, t) * 0.3 + _noise(frames) * 0.15
    return _make_sound(arr * _envelope(frames, 0.005, 0.04, 0.1, 0.02), vol)

def _gen_back(vol=0.45):
    dur = 0.08; frames = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, frames, False)
    arr = _sine(400, t) * 0.6 + _sine(600, t) * 0.3
    return _make_sound(arr * _envelope(frames, 0.005, 0.06, 0.0, 0.01), vol)

def _gen_npc_blip(freq=280, vol=0.4):
    dur = 0.045; frames = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, frames, False)
    arr = _square(freq, t, duty=0.4) * 0.6 + _sine(freq * 1.5, t) * 0.3
    return _make_sound(arr * _envelope(frames, 0.003, 0.025, 0.2, 0.01), vol)

def _gen_npc_notification(vol=0.6):
    """Ping corto que llama la atención al panel de diálogo."""
    dur = 0.22; frames = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, frames, False)
    arr  = _sine(1047, t) * 0.45
    arr += _sine(1319, t) * 0.28
    arr += _sine(1568, t) * 0.15
    return _make_sound(arr * _envelope(frames, 0.005, 0.04, 0.15, 0.12), vol)

def _gen_mission_complete(vol=0.7):
    notes = [523, 659, 784, 1047]; dur_note = 0.18
    total = len(notes) * dur_note + 0.3
    frames = int(SAMPLE_RATE * total)
    arr = np.zeros(frames, dtype=np.float32)
    for i, freq in enumerate(notes):
        s = int(i * dur_note * SAMPLE_RATE); e = s + int(dur_note * SAMPLE_RATE)
        t = np.linspace(0, dur_note, e - s, False)
        note = _sine(freq, t) * 0.5 + _sine(freq * 2, t) * 0.2
        arr[s:e] += note * _envelope(e - s, 0.01, 0.05, 0.6, 0.08)
    return _make_sound(arr, vol)

def _gen_victory(vol=0.75):
    chord = [261, 330, 392, 523, 659]; dur = 1.8; frames = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, frames, False)
    arr = sum(_sine(f, t) * (0.25 - i * 0.03) for i, f in enumerate(chord))
    shimmer = _sine(1200, t) * np.sin(2 * np.pi * 8 * t) * 0.08
    env = _envelope(frames, 0.05, 0.1, 0.8, 0.5)
    return _make_sound((arr + shimmer) * env, vol)

def _gen_minigame_win(vol=0.7):
    notes = [523, 659, 784, 1047, 1319]; dur_note = 0.12
    total = len(notes) * dur_note + 0.2; frames = int(SAMPLE_RATE * total)
    arr = np.zeros(frames, dtype=np.float32)
    for i, freq in enumerate(notes):
        s = int(i * dur_note * SAMPLE_RATE); e = min(frames, s + int(dur_note * SAMPLE_RATE))
        t = np.linspace(0, dur_note, e - s, False)
        arr[s:e] += (_sine(freq, t) * 0.55 + _sine(freq * 2, t) * 0.15) * \
                    _envelope(e - s, 0.008, 0.04, 0.5, 0.06)
    return _make_sound(arr, vol)

def _gen_minigame_lose(vol=0.65):
    notes = [392, 349, 330, 262]; dur_note = 0.22
    total = len(notes) * dur_note + 0.2; frames = int(SAMPLE_RATE * total)
    arr = np.zeros(frames, dtype=np.float32)
    for i, freq in enumerate(notes):
        s = int(i * dur_note * SAMPLE_RATE); e = min(frames, s + int(dur_note * SAMPLE_RATE))
        t = np.linspace(0, dur_note, e - s, False)
        arr[s:e] += (_sine(freq, t) * 0.5 + _sawtooth(freq * 0.5, t) * 0.15) * \
                    _envelope(e - s, 0.01, 0.08, 0.4, 0.1)
    return _make_sound(arr, vol)

def _gen_algo_step(algo_name, vol=0.3):
    freqs = {"bfs": 440, "dfs": 330, "dijkstra": 523, "kruskal": 392, "ff": 262}
    freq = freqs.get(algo_name, 400)
    dur = 0.055; frames = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, frames, False)
    arr = _sine(freq, t) * 0.5 + _sine(freq * 2, t) * 0.2
    return _make_sound(arr * _envelope(frames, 0.004, 0.03, 0.1, 0.01), vol)

def _gen_algo_start(algo_name, vol=0.4):
    freqs = {"bfs": [440,554,660], "dfs": [330,392,494], "dijkstra": [523,659,784],
             "kruskal": [392,494,587], "ff": [262,330,392]}
    chord_freqs = freqs.get(algo_name, [440, 554, 660])
    dur = 0.35; frames = int(SAMPLE_RATE * dur)
    arr = np.zeros(frames, dtype=np.float32)
    for i, freq in enumerate(chord_freqs):
        s = int(i * 0.07 * SAMPLE_RATE)
        seg_t = np.linspace(0, dur - i * 0.07, frames - s, False)
        arr[s:] += _sine(freq, seg_t) * (0.3 - i * 0.05)
    return _make_sound(arr * _envelope(frames, 0.02, 0.05, 0.6, 0.15), vol)

def _gen_config_change(vol=0.35):
    dur = 0.1; frames = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, frames, False)
    arr = _sine(660, t) * 0.4 + _sine(880, t) * 0.3
    return _make_sound(arr * _envelope(frames, 0.005, 0.05, 0.2, 0.04), vol)

def _gen_xp_gain(vol=0.45):
    dur = 0.18; frames = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, frames, False)
    arr = _sine(523, t) * 0.4; mid = frames // 2
    arr[mid:] += _sine(784, t[mid:]) * 0.3
    return _make_sound(arr * _envelope(frames, 0.01, 0.08, 0.3, 0.06), vol)

def _gen_ambient_loop(vol=1.0):
    dur = 4.0; frames = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, frames, False)
    drone  = _sine(55, t) * 0.35 + _sine(82.5, t) * 0.20 + _sine(110, t) * 0.12
    drone *= 0.7 + 0.3 * np.sin(2 * np.pi * 0.25 * t)
    drone += _sine(880, t) * 0.04 * np.sin(2 * np.pi * 0.7 * t)
    fade = 200
    drone[:fade] *= np.linspace(0, 1, fade); drone[-fade:] *= np.linspace(1, 0, fade)
    return _make_sound(drone, vol)

def _gen_menu_music(vol=0.35):
    dur = 8.0; frames = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, frames, False)
    bass = _sine(55, t) * 0.4 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.5 * t))
    pad  = (_sine(220, t) * 0.15 + _sine(277, t) * 0.12 + _sine(330, t) * 0.10) * \
           (0.7 + 0.3 * np.sin(2 * np.pi * 0.13 * t))
    arp_freqs = [523, 659, 784, 659]; arp_dur = 0.5
    arp = np.zeros(frames, dtype=np.float32)
    for i in range(int(dur / arp_dur)):
        freq = arp_freqs[i % len(arp_freqs)]
        s = int(i * arp_dur * SAMPLE_RATE); e = min(frames, s + int(arp_dur * SAMPLE_RATE))
        seg_t = np.linspace(0, arp_dur, e - s, False)
        arp[s:e] += _sine(freq, seg_t) * 0.12 * _envelope(e - s, 0.01, 0.1, 0.3, 0.15)
    arr = bass + pad + arp
    fade = 800
    arr[:fade] *= np.linspace(0, 1, fade); arr[-fade:] *= np.linspace(1, 0, fade)
    return _make_sound(arr, vol)

def _gen_minigame_trigger(vol=0.55):
    dur = 0.5; frames = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, frames, False)
    arr = _sine(523, t) * 0.3 + _sine(784, t) * 0.2 + \
          _square(200, t, 0.3) * 0.1 * np.sin(2 * np.pi * 4 * t)
    return _make_sound(arr * _envelope(frames, 0.03, 0.1, 0.5, 0.25), vol)


# ──────────────────────────────────────────────────────────
#  CLASE PRINCIPAL
# ──────────────────────────────────────────────────────────

class SoundManager:
    CH_SFX     = 0
    CH_NPC     = 1
    CH_ALGO    = 2
    CH_AMBIENT = 3
    CH_MUSIC   = 4
    CH_NOTIF   = 5   # canal dedicado para ping de notificación NPC

    def __init__(self):
        if not pygame.get_init():
            pygame.init()
        try:
            pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=1024)
            pygame.mixer.set_num_channels(8)
            self._ok = True
        except Exception as e:
            print(f"[SoundManager] No se pudo iniciar mixer: {e}")
            self._ok = False
            return

        self._volume = 0.5
        self._ambient_playing = False
        self._music_playing   = False

        print("[SoundManager] Generando sonidos procedurales...")
        self._sounds = {
            "click":        _gen_click(),
            "back":         _gen_back(),
            "mission_done": _gen_mission_complete(),
            "victory":      _gen_victory(),
            "minigame_win": _gen_minigame_win(),
            "minigame_lose":_gen_minigame_lose(),
            "config":       _gen_config_change(),
            "xp":           _gen_xp_gain(),
            "ambient":      _gen_ambient_loop(),
            "menu_music":   _gen_menu_music(),
            "mg_trigger":   _gen_minigame_trigger(),
            "npc_notif":    _gen_npc_notification(),
        }
        for algo in ("bfs", "dfs", "dijkstra", "kruskal", "ff"):
            self._sounds[f"step_{algo}"]  = _gen_algo_step(algo)
            self._sounds[f"start_{algo}"] = _gen_algo_start(algo)

        self._npc_blips = [_gen_npc_blip(freq) for freq in
                           [220, 262, 294, 330, 349, 392, 440, 494]]
        self._npc_blip_timer    = 0
        self._npc_blip_interval = 3

        self._apply_volume()
        print("[SoundManager] ✓ Sonidos listos.")

    # ── Volumen ─────────────────────────────────────────
    def set_volume(self, vol: float):
        self._volume = max(0.0, min(1.0, vol))
        self._apply_volume()

    def get_volume(self):
        return self._volume

    def _apply_volume(self):
        if not self._ok: return
        v = self._volume
        for snd in self._sounds.values():
            snd.set_volume(v)
        for b in self._npc_blips:
            b.set_volume(v * 0.8)
        try:
            pygame.mixer.Channel(self.CH_AMBIENT).set_volume(v * 0.9)
            pygame.mixer.Channel(self.CH_MUSIC).set_volume(v)
        except Exception:
            pass

    # ── Reproducción general ────────────────────────────
    def play(self, name: str, channel=None):
        if not self._ok: return
        snd = self._sounds.get(name)
        if snd is None: return
        if channel is not None:
            pygame.mixer.Channel(channel).play(snd)
        else:
            snd.play()

    # ── UI ───────────────────────────────────────────────
    def play_click(self):              self.play("click",        self.CH_SFX)
    def play_back(self):               self.play("back",         self.CH_SFX)
    def play_config_change(self):      self.play("config",       self.CH_SFX)
    def play_xp(self):                 self.play("xp",           self.CH_SFX)
    def play_mission_complete(self):   self.play("mission_done", self.CH_SFX)
    def play_victory(self):            self.play("victory",      self.CH_SFX)
    def play_minigame_win(self):       self.play("minigame_win", self.CH_SFX)
    def play_minigame_lose(self):      self.play("minigame_lose",self.CH_SFX)
    def play_minigame_trigger(self):   self.play("mg_trigger",   self.CH_SFX)

    def play_npc_notification(self):
        """Ping que llama la atención al panel de diálogo inferior-izquierdo."""
        self.play("npc_notif", self.CH_NOTIF)

    # ── Algoritmos ──────────────────────────────────────
    def play_algo_start(self, algo_name: str): self.play(f"start_{algo_name}", self.CH_ALGO)
    def play_algo_step(self, algo_name: str):  self.play(f"step_{algo_name}",  self.CH_ALGO)

    # ── NPC blips (Undertale style) ─────────────────────
    def tick_npc_talking(self, is_talking: bool):
        if not self._ok or not is_talking:
            self._npc_blip_timer = 0; return
        self._npc_blip_timer += 1
        if self._npc_blip_timer >= self._npc_blip_interval:
            self._npc_blip_timer = 0
            blip = random.choice(self._npc_blips)
            ch = pygame.mixer.Channel(self.CH_NPC)
            if not ch.get_busy():
                ch.play(blip)

    # ── Música y ambiente ───────────────────────────────
    def start_menu_music(self):
        if not self._ok or self._music_playing: return
        pygame.mixer.Channel(self.CH_AMBIENT).stop()
        pygame.mixer.Channel(self.CH_MUSIC).play(self._sounds["menu_music"], loops=-1)
        self._music_playing = True
        self._ambient_playing = False

    def start_ambient(self, force=False):
        if not self._ok: return
        if self._ambient_playing and not force: return
        pygame.mixer.Channel(self.CH_MUSIC).stop()
        ch = pygame.mixer.Channel(self.CH_AMBIENT)
        ch.play(self._sounds["ambient"], loops=-1)
        ch.set_volume(self._volume * 0.9)
        self._ambient_playing = True
        self._music_playing = False

    def stop_all_music(self):
        if not self._ok: return
        pygame.mixer.Channel(self.CH_MUSIC).stop()
        pygame.mixer.Channel(self.CH_AMBIENT).stop()
        self._music_playing = False
        self._ambient_playing = False


# ── Instancia global ────────────────────────────────────────
_instance: SoundManager = None

def get_sound_manager() -> SoundManager:
    global _instance
    if _instance is None:
        _instance = SoundManager()
    return _instance
