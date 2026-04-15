@echo off
cd /d C:\Users\Joshyoh\.openclaw\workspace\eldercare-project\code
del /s /q __pycache__ 2>nul
python run.py
pause