@echo off
cd /d C:\Users\Joshyoh\.openclaw\workspace\eldercare-project\code
echo Starting Flask on port 5000...
start /b python app.py
timeout /t 3 /nobreak >nul
echo Starting ngrok tunnel...
"C:\Users\Joshyoh\AppData\Local\Microsoft\WinGet\Packages\Ngrok.Ngrok_Microsoft.Winget.Source_8wekyb3d8bbwe\ngrok.exe" http 5000
pause