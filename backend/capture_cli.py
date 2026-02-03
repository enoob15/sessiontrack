#!/usr/bin/env python3
import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import asyncio
import argparse

try:
    import google.generativeai as genai
except ImportError:
    print("Gemini AI library not installed. Some features will be limited.")
    genai = None

class SessionCapture:
    def __init__(self, 
                 base_path: str = '/root/clawd/sessions_archive', 
                 gemini_api_key: Optional[str] = None):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
        
        # Initialize Gemini AI if possible
        if genai and gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        else:
            self.gemini_model = None

    async def capture_session(self, 
                        session_key: str, 
                        source: str, 
                        messages: List[Dict],
                        project: Optional[str] = None) -> str:
        """
        Capture a complete session with metadata and AI-enhanced processing
        
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
        
        # Extract participants
        participants = list(set(
            msg.get('author', 'unknown') for msg in messages
        ))
        
        # Prepare session data
        session_data = {
            'id': session_id,
            'session_key': session_key,
            'timestamp': timestamp,
            'source': source,
            'project': project,
            'total_messages': len(messages),
            'participants': participants,
            'messages': messages
        }
        
        # AI-Powered Enhancements
        await self._enhance_session_metadata(session_data)
        
        # Save session file
        filename = f"{timestamp}_{session_id}.json"
        filepath = os.path.join(self.base_path, filename)
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        return filepath

    async def _enhance_session_metadata(self, session_data: Dict):
        """
        Use Gemini AI to enhance session metadata
        """
        if not self.gemini_model:
            return
        
        try:
            # Extract conversation text
            conversation_text = "\n".join([
                f"{msg.get('author', 'Unknown')}: {msg.get('content', '')}" 
                for msg in session_data['messages']
            ])
            
            # Generate summary
            summary_prompt = f"""
            Provide a concise summary of the following conversation. 
            Identify key discussion points, decisions made, 
            and any actionable items.

            Conversation:
            {conversation_text}
            """
            
            summary_response = await self.gemini_model.generate_content_async(summary_prompt)
            
            # Add AI-generated insights
            session_data['ai_summary'] = summary_response.text
            session_data['ai_topics'] = self._extract_topics(summary_response.text)
        
        except Exception as e:
            print(f"AI enhancement error: {e}")
            session_data['ai_summary'] = "AI summarization failed"

    def _extract_topics(self, summary: str) -> List[str]:
        """
        Basic topic extraction from summary
        """
        # This is a placeholder - in production, use more sophisticated NLP
        common_topics = [
            'project management', 'ai', 'technology', 
            'development', 'strategy', 'automation'
        ]
        return [
            topic for topic in common_topics 
            if topic.lower() in summary.lower()
        ]

async def main():
    parser = argparse.ArgumentParser(description='SessionTrack Capture CLI')
    parser.add_argument('--source', default='cli', help='Session source')
    parser.add_argument('--project', help='Project name')
    parser.add_argument('--gemini-key', help='Gemini API Key for AI enhancements')
    
    args = parser.parse_args()
    
    # Interactive session capture
    print("SessionTrack CLI - Conversation Capture")
    print("Enter your messages. Type 'END' on a new line to finish.")
    
    messages = []
    current_author = None
    
    while True:
        if not current_author:
            current_author = input("Enter your name/identifier: ")
        
        message_content = input(f"{current_author}: ")
        
        if message_content.strip().upper() == 'END':
            break
        
        messages.append({
            'author': current_author,
            'content': message_content,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    # Capture session
    capture = SessionCapture(gemini_api_key=args.gemini_key)
    session_file = await capture.capture_session(
        session_key='manual:cli',
        source=args.source,
        messages=messages,
        project=args.project
    )
    
    print(f"Session captured: {session_file}")

if __name__ == '__main__':
    asyncio.run(main())