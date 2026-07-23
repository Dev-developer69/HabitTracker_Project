"""
Launcher for the Habit Tracker .exe
- Boots Streamlit programmatically so it runs from a standalone
  PyInstaller .exe (no Python install needed on the target PC).
- SINGLE INSTANCE ONLY: if the app is already running (port already
  bound), clicking the exe again just opens a new browser tab to the
  existing server instead of starting a duplicate process. This is
  what was causing many "HabitTracker" entries to pile up in Task
  Manager when the exe was double-clicked multiple times.
"""

import os
import sys
import socket
import threading
import webbrowser
import time

PORT = 8501


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller .exe"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def is_port_in_use(port):
    """Returns True if something is already listening on this port
    (i.e. the app is already running)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:
            s.connect(("127.0.0.1", port))
            return True
        except (ConnectionRefusedError, OSError):
            return False


def open_browser(delay=2):
    time.sleep(delay)
    webbrowser.open(f"http://localhost:{PORT}")


if __name__ == "__main__":
    # --- Single instance check -------------------------------------------
    if is_port_in_use(PORT):
        # App is already running somewhere -> just open a browser tab
        # to it and exit immediately. Do NOT start a second server.
        webbrowser.open(f"http://localhost:{PORT}")
        sys.exit(0)

    # --- Not running yet -> start the Streamlit server normally ----------
    from streamlit.web import cli as stcli

    app_path = resource_path("app.py")

    threading.Thread(target=open_browser, daemon=True).start()

    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
        "--server.headless=true",
        "--server.port=" + str(PORT),
        "--browser.gatherUsageStats=false",
        "--client.toolbarMode=minimal",
    ]
    sys.exit(stcli.main())
