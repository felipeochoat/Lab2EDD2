"""
network/server.py  —  Servidor de multijugador local (NetGuardian)
==================================================================
El servidor corre en un HILO de fondo dentro del mismo proceso del juego.
Su único trabajo: recibir el estado del teclado del Jugador 2 (flechas)
desde el cliente, y ponerlo disponible para el juego principal.

Protocolo (texto plano, una línea JSON por mensaje):
  Cliente  →  Servidor :  {"left": bool, "right": bool, "up": bool}
  Servidor →  Cliente  :  {"ok": true}   (ACK simple)
"""

import socket
import threading
import json


HOST = "127.0.0.1"   # solo local; para red cambiar a "0.0.0.0"
PORT = 54321


class GameServer:
    """
    Servidor TCP de un cliente.  Arranca con start() en un hilo daemon.
    El juego lee self.p2_keys cada frame para mover al Jugador 2.
    """

    def __init__(self):
        # Estado de teclas del J2, compartido con el hilo principal
        self.p2_keys   = {"left": False, "right": False, "up": False}
        self._lock     = threading.Lock()
        self.connected = False      # True cuando hay un cliente activo
        self._running  = False

    # ── API pública ───────────────────────────────────────────────────────

    def start(self):
        """Lanza el hilo servidor en segundo plano."""
        self._running = True
        t = threading.Thread(target=self._accept_loop, daemon=True)
        t.start()

    def stop(self):
        self._running = False

    def get_p2_keys(self):
        """Devuelve una copia hilo-segura del estado de teclas del J2."""
        with self._lock:
            return dict(self.p2_keys)

    # ── Bucle interno ─────────────────────────────────────────────────────

    def _accept_loop(self):
        """Espera conexiones en un socket TCP."""
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(1)
        srv.settimeout(1.0)
        print(f"[SERVER] Esperando al J2 en {HOST}:{PORT}…")

        while self._running:
            try:
                conn, addr = srv.accept()
                print(f"[SERVER] J2 conectado desde {addr}")
                self.connected = True
                self._handle_client(conn)
            except socket.timeout:
                continue
            except OSError:
                break

        srv.close()

    def _handle_client(self, conn):
        """Recibe líneas JSON del cliente con el estado de teclas."""
        buf = ""
        try:
            while self._running:
                data = conn.recv(256).decode(errors="ignore")
                if not data:
                    break
                buf += data
                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        keys = json.loads(line)
                        with self._lock:
                            self.p2_keys = keys
                        # ACK mínimo
                        conn.sendall(b'{"ok":true}\n')
                    except json.JSONDecodeError:
                        pass
        except (OSError, ConnectionResetError):
            pass
        finally:
            conn.close()
            self.connected = False
            with self._lock:
                self.p2_keys = {"left": False, "right": False, "up": False}
            print("[SERVER] J2 desconectado.")
