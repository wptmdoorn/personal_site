from nicegui import app
import importlib
from fastapi.middleware.wsgi import WSGIMiddleware
import os
import urllib.error
import urllib.request


# Pull the Labkompas front-end straight from the separate nhg-labkompas repo so
# this site never keeps a permanent copy and serves the newest version on each
# (re)start. It's a folder, not a single file: the HTML loads ./support.js and
# fetches ./data/labkompas.json at runtime, so all three are downloaded into the
# same static base path. We serve them ourselves (correct text/html), because
# raw.githubusercontent.com / jsDelivr return text/plain and won't render.
_LABKOMPAS_RAW = "https://raw.githubusercontent.com/wptmdoorn/nhg-labkompas/main"
_LABKOMPAS_FILES = ["Labkompas.dc.html", "support.js", "data/labkompas.json"]
_LABKOMPAS_DEST = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "static", "labkompas"))


def fetch_labkompas(dest_dir: str = _LABKOMPAS_DEST) -> None:
    """Best-effort download of the latest Labkompas files into the static dir.

    On any network/HTTP error the existing (possibly stale) files are kept, so a
    GitHub outage or a not-yet-published data file never blocks app startup.
    """
    for rel in _LABKOMPAS_FILES:
        url = f"{_LABKOMPAS_RAW}/{rel}"
        target = os.path.join(dest_dir, *rel.split("/"))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = resp.read()
            with open(target, "wb") as f:
                f.write(data)
            print(f"[labkompas] fetched {rel} ({len(data)} bytes)")
        except urllib.error.HTTPError as e:
            note = "not in repo yet" if e.code == 404 else f"HTTP {e.code}"
            print(f"[labkompas] {rel}: {note} - keeping existing copy")
        except Exception as e:  # noqa: BLE001 - startup must not crash on network
            print(f"[labkompas] {rel}: {e} - keeping existing copy")


def register_dash_apps():
    for f in os.listdir('app/software'):
        if os.path.isdir(f'app/software/{f}'):
            page_module = importlib.import_module(f'software.{f}.main')

            if page_module.SOFTWARE_TYPE == 'DASH':
                dash_app = page_module.page(
                    requests_pathname_prefix=f'/software/dash/{f}/')

                app.mount(f'/software/dash/{f}/',
                          WSGIMiddleware(dash_app.server))
