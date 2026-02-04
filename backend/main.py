from fastapi import FastAPI
from api import sessions, projects

app = FastAPI(title="SessionTrack API")

# Include routers from individual API modules
app.include_router(sessions.router)
app.include_router(projects.router)