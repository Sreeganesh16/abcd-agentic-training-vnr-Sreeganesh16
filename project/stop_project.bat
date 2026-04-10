@echo off
setlocal

echo Stopping Python servers using port 5001...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5001') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo Done.

endlocal
