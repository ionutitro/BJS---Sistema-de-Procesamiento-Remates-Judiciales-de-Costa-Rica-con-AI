@echo off
echo Starting BJS Backend Server...
cd c:\xampp\htdocs\BJS
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
pause
