"""
network/client.py  —  Cliente de multijugador local (NetGuardian)
=================================================================
Corre en un HILO de fondo dentro del mismo proceso del juego (J2).
Envía al servidor el estado de las teclas de flecha cada vez que
el juego llama a send_keys().

Protocolo: igual que server.py (JSON + salto de línea).
"""

import socket
import threading
import json


PORT = 54321


class GameClient:
    """
    Cliente TCP.  Conecta con connect(host) y luego el juego llama
    send_keys() cada frame para transmitir el estado de las flechas.
    """

    def __init__(self):
        self.connected = False
        self.error     = ""
        self._sock     = None
        self._lock     = threading.Lock()

    # ── API pública ───────────────────────────────────────────────────────

    def connect(self, host: str = "127.0.0.1") -> bool:
        """Intenta conectar al servidor. Devuelve True si tuvo éxito."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect((host, PORT))
            sock.settimeout(None)
            self._sock     = sock
            self.connected = True
            # Hilo de fondo solo para leer los ACKs (no bloquear el juego)
            t = threading.Thread(target=self._recv_loop, daemon=True)
            t.start()
            print(f"[CLIENT] Conectado al servidor en {host}:{PORT}")
            return True
        except (ConnectionRefusedError, socket.timeout, OSError) as e:
            self.error     = str(e)
            self.connected = False
            return False

    def send_keys(self, left: bool, right: bool, up: bool):
        """Envía el estado de teclas al servidor (llamado cada frame)."""
        if not self.connected or self._sock is None:
            return
        msg = json.dumps({"left": left, "right": right, "up": up}) + "\n"
        try:
            with self._lock:
                self._sock.sendall(msg.encode())
        except OSError:
            self.connected = False

    def stop(self):
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
        self.connected = False

    # ── Bucle interno ─────────────────────────────────────────────────────

    def _recv_loop(self):
        """Descarta los ACKs del servidor para no bloquear el buffer."""
        try:
            while self.connected:
                data = self._sock.recv(64)
                if not data:
                    break
        except OSError:
            pass
        finally:
            self.connected = False
            print("[CLIENT] Desconectado del servidor.")
