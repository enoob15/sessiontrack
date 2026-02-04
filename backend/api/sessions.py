import os
import json
from fastapi import APIRouter, HTTPException
from typing import List, Dict

router = APIRouter(prefix="/sessions", tags=["sessions"])

SESSIONS_ARCHIVE = '/root/clawd/sessions_archive'

@router.get("/", response_model=List[Dict])
async def list_sessions():
    """
    Retrieve list of captured sessions
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
                
                # Prepare session summary
                sessions.append({
                    'id': session_data.get('id'),
                    'timestamp': session_data.get('timestamp'),
                    'project': session_data.get('project'),
                    'participants': session_data.get('participants', []),
                    'total_messages': session_data.get('total_messages', 0),
                    'ai_insights': session_data.get('ai_insights', {})
                })
        
        return sessions
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sessions: {str(e)}")

@router.get("/{session_id}", response_model=Dict)
async def get_session(session_id: str):
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