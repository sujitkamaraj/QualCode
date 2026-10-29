@echo off
cd /d "%~dp0"
where py >nul 2>nul && (py server.py) || (python server.py)
if errorlevel 1 (
  echo.
  echo Python was not found. Install it from https://www.python.org/downloads/ and tick "Add Python to PATH".
)
pause
