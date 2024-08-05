@echo off
echo Starting the Discord bot...

REM Navigate to the directory where the bot is located
cd /d %~dp0

REM Run the bot
python main.py

REM Pause to keep the window open if there's an error
pause
