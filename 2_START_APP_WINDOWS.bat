@echo off
cd /d "%~dp0"
echo Calculator will open at http://127.0.0.1:8000
start "" "http://127.0.0.1:8000"
py -m uvicorn main:app --reload
pause
