import os
import json
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SESSIONS_ARCHIVE = '/root/clawd/sessions_archive'

@app.get("/sessions")
async def list_sessions() -> List[Dict]:
    """
    List all captured sessions with basic metadata
    """
    try:
        # Get all JSON files in the sessions archive
        session_files = [f for f in os.listdir(SESSIONS_ARCHIVE) if f.endswith('.json')]
        
        # Sort files by timestamp (newest first)
        session_files.sort(reverse=True)
        
        # Load session metadata
        sessions = []
        for filename in session_files[:50]:  # Limit to last 50 sessions
            filepath = os.path.join(SESSIONS_ARCHIVE, filename)
            with open(filepath, 'r') as f:
                session_data = json.load(f)
                # Trim down the data to essential metadata
                sessions.append({
                    'id': session_data.get('id', filename),
                    'timestamp': session_data.get('timestamp'),
                    'project': session_data.get('project'),
                    'participants': session_data.get('participants', []),
                    'total_messages': session_data.get('total_messages', 0),
                    'ai_summary': session_data.get('ai_summary')
                })
        
        return sessions
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sessions: {str(e)}")

@app.get("/sessions/{session_id}")
async def get_session(session_id: str) -> Dict:
    """
    Retrieve full details of a specific session
    """
    try:
        # Find the session file
        for filename in os.listdir(SESSIONS_ARCHIVE):
            if session_id in filename and filename.endswith('.json'):
                filepath = os.path.join(SESSIONS_ARCHIVE, filename)
                with open(filepath, 'r') as f:
                    return json.load(f)
        
        raise HTTPException(status_code=404, detail="Session not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving session: {str(e)}")