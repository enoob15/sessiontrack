#!/usr/bin/env python3
import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional

class SessionCapture:
    def __init__(self, base_path: str = '/root/clawd/sessions_archive'):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def capture_session(self, 
                        session_key: str, 
                        source: str, 
                        messages: List[Dict],
                        project: Optional[str] = None) -> str:
        """
        Capture a complete session with metadata
        
        Args:
            session_key: Unique session identifier
            source: Origin of the session (webchat, cli, etc.)
            messages: List of conversation messages
            project: Optional project name
        
        Returns:
            Path to saved session file
        """
        session_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        session_data = {
            'id': session_id,
            'session_key': session_key,
            'timestamp': timestamp,
            'source': source,
            'project': project,
            'total_messages': len(messages),
            'messages': messages
        }
        
        # Additional metadata extraction
        session_data['participants'] = list(set(
            msg.get('author', 'unknown') for msg in messages
        ))
        
        # Simple AI-powered topic extraction (placeholder)
        session_data['primary_topic'] = self._extract_primary_topic(messages)
        
        # Save session file
        filename = f"{timestamp}_{session_id}.json"
        filepath = os.path.join(self.base_path, filename)
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        return filepath

    def _extract_primary_topic(self, messages: List[Dict]) -> str:
        """
        Basic topic extraction (to be enhanced with AI in future)
        """
        # This is a very naive implementation
        # In production, use semantic analysis or AI
        topics = {}
        for msg in messages:
            text = msg.get('content', '').lower()
            for topic in ['project', 'code', 'ai', 'tool', 'automation']:
                if topic in text:
                    topics[topic] = topics.get(topic, 0) + 1
        
        return max(topics, key=topics.get) if topics else 'uncategorized'

def main():
    # Example usage
    capture = SessionCapture()
    
    # Simulated session data
    sample_messages = [
        {
            'author': 'Human',
            'content': 'Let\'s discuss our new SessionTrack project',
            'timestamp': datetime.utcnow().isoformat()
        },
        {
            'author': 'TARS',
            'content': 'Great! I\'ve started outlining the requirements',
            'timestamp': datetime.utcnow().isoformat()
        }
    ]
    
    session_file = capture.capture_session(
        session_key='main:webchat',
        source='webchat',
        messages=sample_messages,
        project='SessionTrack'
    )
    
    print(f"Session captured: {session_file}")

if __name__ == '__main__':
    main()