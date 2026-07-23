# Habit Tracker (Streamlit, Local, JSON storage)

A local habit tracker app — daily check-in, spreadsheet-style monthly grid,
and progress charts — inspired by the Google Sheets habit tracker.

No internet, no Supabase, no login needed. Everything is stored in a
plain `habit_data.json` file next to the app.

## Files

- `app.py` — the Streamlit app (3 tabs: Daily Check-in, Grid View, Progress & Charts)
- `run_app.py` — launcher used to build the standalone .exe
- `habit_tracker.spec` — PyInstaller spec file
- `build_exe.bat` — one-click Windows build script
- `requirements.txt` — Python dependencies
- `habit_data.json` — created automatically on first run (your data)

## 1. Run locally with Python (development / testing)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`.

## 2. Features

- **Setup**: click the **⚙️ Setup** button (top-right) to add/remove habits and
  set/edit monthly goals — opens as a popup, no sidebar needed.
- **Top navigation buttons**: switch between Daily Check-in / Grid View /
  Progress & Charts using the pill-style buttons at the top (no tabs, no
  Streamlit toolbar/Deploy bar — fully hidden for a clean, distraction-free look).
- **Daily Check-in tab**: pick a date, tick off habits for that day,
  see today's completion %.
- **Grid View tab**: spreadsheet-style table — habits as rows, every day
  of the selected month as a checkbox column, plus Goal/Completed/% columns.
  Tick boxes directly in the grid; it auto-saves.
- **Progress & Charts tab**: weekly bar chart (like the orange bars in the
  sheet), per-habit progress bars, and overall month stats. Shows a friendly
  message instead of a broken-looking chart when no check-ins exist yet.

## 3. Build a standalone .exe (no Python needed on target PC)

On a **Windows machine** with Python installed:

```cmd
build_exe.bat
```

This will:
1. Create a virtual environment (`venv`)
2. Install all dependencies
3. Run PyInstaller using `habit_tracker.spec`
4. Output everything into `dist\HabitTracker\`

To distribute: copy the entire `dist\HabitTracker` folder to the target
PC (e.g. via USB or zip it). Run `HabitTracker.exe` inside that folder —
it will open your default browser at `http://localhost:8501` automatically.

> Note: copy the **whole folder**, not just the .exe — PyInstaller bundles
> Streamlit's runtime/static files alongside it (this is normal, same as
> with your Fleet Manager .exe).

### Manual build (without the .bat)

```cmd
pip install -r requirements.txt
pyinstaller habit_tracker.spec --noconfirm
```

### Windows 7 compatibility note

Same caveats as your Fleet Manager packaging: build the .exe using a
Python version that still supports Windows 7 (Python 3.8 is the safest
bet — Python 3.9+ dropped official Win7 support). If the target PC is
Windows 7, install Python 3.8 in your build venv before running
`build_exe.bat`.

## 4. Data file

`habit_data.json` is created next to the .exe (or next to app.py when run
via Python) on first launch — this is your full habit history. Back it up
by simply copying that file; restore by placing it back in the same folder.
