# Backward-compatible module.
# The FastAPI backend now lives in app.py.
# You can run either:
#   uvicorn app:app --reload
# or:
#   uvicorn api:app --reload

from app import app
