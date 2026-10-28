@echo off
cd /d "%~dp0"
echo Installing Python packages...
py -m pip install -r requirements.txt
if errorlevel 1 goto failed
echo Installing Playwright Chromium...
py -m playwright install chromium
if errorlevel 1 goto failed
echo.
echo Setup completed. Use 2_START_APP_WINDOWS.bat to start the calculator.
pause
exit /b 0
:failed
echo.
echo SETUP ERROR: Copy the error message and ask for help.
pause
exit /b 1
