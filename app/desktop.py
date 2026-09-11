"""Entrypoint desktop: sobe o servidor local em loopback e abre uma janela nativa."""

import base64
import socket
import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser

import uvicorn
import webview

from .main import app

WINDOW_TITLE = "Conversor DBC (Datasus) -> Excel"
HEALTH_TIMEOUT_SECONDS = 10


class DesktopApi:
    """Exposta ao frontend como `window.pywebview.api`.

    O download via `<a download>`/blob-URL (usado no navegador) não abre o
    diálogo "Salvar como" dentro da janela nativa do pywebview — por isso o
    salvamento real do .xlsx passa por aqui, usando o file dialog nativo do SO.
    """

    def __init__(self) -> None:
        self._window: "webview.Window | None" = None

    def set_window(self, window: "webview.Window") -> None:
        self._window = window

    def save_file(self, filename: str, base64_data: str) -> dict:
        if self._window is None:
            return {"ok": False, "error": "Janela nao inicializada."}

        try:
            path = self._window.create_file_dialog(
                webview.SAVE_DIALOG, save_filename=filename
            )
        except Exception as exc:
            return {"ok": False, "error": f"Nao foi possivel abrir a janela de salvar: {exc}"}

        if not path:
            return {"ok": False, "error": None}  # usuario cancelou

        if isinstance(path, (list, tuple)):
            path = path[0]

        try:
            with open(path, "wb") as f:
                f.write(base64.b64decode(base64_data))
            return {"ok": True, "path": path}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_until_ready(url: str, timeout: float) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                if resp.status == 200:
                    return True
        except (urllib.error.URLError, OSError):
            time.sleep(0.1)
    return False


def main() -> None:
    port = _free_port()
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)

    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()

    base_url = f"http://127.0.0.1:{port}"
    if not _wait_until_ready(f"{base_url}/health", HEALTH_TIMEOUT_SECONDS):
        print("Nao foi possivel iniciar o servidor local. Feche o programa e tente novamente.")
        server.should_exit = True
        server_thread.join(timeout=5)
        sys.exit(1)

    try:
        api = DesktopApi()
        window = webview.create_window(
            WINDOW_TITLE, base_url, js_api=api, width=960, height=720, min_size=(720, 560)
        )
        api.set_window(window)
        webview.start()
    except Exception:
        # WebView2 (Windows) ou WKWebView (macOS) indisponivel: usa o navegador padrao como alternativa
        webbrowser.open(base_url)
        print(f"Nao foi possivel abrir a janela nativa. Abrindo {base_url} no navegador padrao.")
        print("Feche este terminal para encerrar o programa.")
        try:
            while server_thread.is_alive():
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass

    server.should_exit = True
    server_thread.join(timeout=5)


if __name__ == "__main__":
    main()
