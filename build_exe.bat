@echo off
echo ============================================
echo  Building Habit Tracker .exe (Windows)
echo ============================================

REM 1. Create / activate a virtual environment (optional but recommended)
IF NOT EXIST venv (
    python -m venv venv
)
call venv\Scripts\activate

REM 2. Install dependencies
pip install -r requirements.txt

REM 3. Build with PyInstaller using the spec file
pyinstaller habit_tracker.spec --noconfirm

echo.
echo Build complete! Find your app in:
echo   dist\HabitTracker\HabitTracker.exe
echo.
echo Copy the entire "dist\HabitTracker" folder to the target PC
echo and run HabitTracker.exe from there. A browser tab will open
echo automatically at http://localhost:8501
pause
