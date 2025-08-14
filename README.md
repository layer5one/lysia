# Elysia: Local AI Companion

## Setup
1. Install backend deps: `pip install -r backend/requirements.txt`
2. Pull model: `ollama pull elysia:latest`
3. Run Ollama server.
4. Start backend: `python backend/main.py`
5. Start frontend: `cd frontend && npm start`
6. For monitoring: `bash utils/watchdog.sh`

## Features
- Voice interaction with selective memory.
- Real-time audio visualization and avatar states.
- No tools or summarization; pure conversation.

Adjust memory threshold in memory.py for more/less recall.
