@echo off
echo Starting AqAI Web Application...
cd ai
python -m flask run --host=0.0.0.0 --port=5000 --debug
pause 