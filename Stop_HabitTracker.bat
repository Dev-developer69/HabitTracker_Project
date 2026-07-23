@echo off
echo Stopping Habit Tracker...
taskkill /F /IM HabitTracker.exe /T >nul 2>&1
echo Done. You can close this window.
pause
