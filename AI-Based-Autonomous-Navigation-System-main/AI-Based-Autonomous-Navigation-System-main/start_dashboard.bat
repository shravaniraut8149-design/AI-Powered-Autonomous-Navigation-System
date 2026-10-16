@echo off
setlocal
cd /d "%~dp0"
title AI-Based Autonomous Navigation Dashboard

echo ================================================
echo   AI-Based Autonomous Navigation System
echo   Local Light-Theme Dashboard
echo ================================================
echo.

if not exist ".venv\Scripts\python.exe" (
  echo Creating Python environment...
  py -m venv .venv
  if errorlevel 1 goto failed
)

.venv\Scripts\python.exe -c "import flask, numpy, matplotlib" >nul 2>&1
if errorlevel 1 (
  echo Installing required packages. This may take a few minutes...
  .venv\Scripts\python.exe -m pip install --upgrade pip
  if errorlevel 1 goto failed
  .venv\Scripts\python.exe -m pip install -r requirements.txt
  if errorlevel 1 goto failed
)

start "" /B cmd /c "timeout /t 3 /nobreak >nul & start http://127.0.0.1:5000"
echo Starting dashboard at http://127.0.0.1:5000
echo Keep this window open while using the dashboard.
echo Press Ctrl+C here to stop the server.
echo.
.venv\Scripts\python.exe web_app.py
goto end

:failed
echo.
echo Setup failed. Please check the error above and ensure Python is installed.
pause
goto end

:end
endlocal
