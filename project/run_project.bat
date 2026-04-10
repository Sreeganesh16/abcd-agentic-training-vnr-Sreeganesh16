@echo off
setlocal

cd /d "%~dp0"

echo Starting Flask backend on port 5001...
start "Context-Aware Backend" cmd /k python -c "from app import app; app.run(debug=False, port=5001)"

timeout /t 3 /nobreak >nul

echo Opening frontend dashboard...
start "" "%~dp0frontend\index.html"

echo.
echo Project started.
echo Backend: http://127.0.0.1:5001
echo Frontend: frontend\index.html

endlocal
