@echo off
cd /d "%~dp0"
py -m pytest -v
pause
