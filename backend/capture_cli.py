#!/usr/bin/env python3
import os
import json
import uuid
from datetime import datetime, UTC
from typing import Dict, List, Optional
import asyncio
import argparse
import sys

# Verbose logging
print(f"Python Version: {sys.version}", file=sys.stderr)
print(f"Environment Variables:", file=sys.stderr)
for key, value in os.environ.items():
    print(f"{key}: {value[:10]}..." if len(value) > 10 else f"{key}: {value}", file=sys.stderr)

# Use environment variable for Gemini key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
print(f"Gemini API Key present: {bool(GEMINI_API_KEY)}", file=sys.stderr)

try:
    import google.generativeai as genai
    print("Gemini library successfully imported", file=sys.stderr)
except ImportError as e:
    print(f"Gemini library import error: {e}", file=sys.stderr)
    genai = None

class SessionCapture:
    def __init__(self, 
                 base_path: str = '/root/clawd/sessions_archive'):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
        
        # Initialize Gemini AI
        if genai and GEMINI_API_KEY:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                print("Gemini model initialized successfully", file=sys.stderr)
            except Exception as e:
                print(f"Gemini model initialization error: {e}", file=sys.stderr)
                self.gemini_model = None
        else:
            print("Gemini AI not configured. AI features will be disabled.", file=sys.stderr)
            self.gemini_model = None

    async def capture_session(self, 
                        session_key: str, 
                        source: str, 
                        messages: List[Dict],
                        project: Optional[str] = None) -> str:
        """
        Capture a complete session with metadata and AI-enhanced processing
        """
        session_id = str(uuid.uuid4())
        timestamp = datetime.now(UTC).isoformat()
        
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
            print("No Gemini model available for enhancement", file=sys.stderr)
            return
        
        try:
            # Extract conversation text
            conversation_text = "\n".join([
                f"{msg.get('author', 'Unknown')}: {msg.get('content', '')}" 
                for msg in session_data['messages']
            ])
            
            # Generate summary
            summary_prompt = f"""
            Analyze the following conversation and provide:
            1. A concise summary
            2. Key discussion topics
            3. Potential action items
            4. Suggested next steps

            Conversation:
            {conversation_text}
            """
            
            print("Generating AI summary...", file=sys.stderr)
            summary_response = await self.gemini_model.generate_content_async(summary_prompt)
            
            # Add AI-generated insights
            session_data['ai_summary'] = summary_response.text
            session_data['ai_topics'] = self._extract_topics(summary_response.text)
            session_data['ai_action_items'] = self._extract_action_items(summary_response.text)
            
            print("AI enhancement completed successfully", file=sys.stderr)
        
        except Exception as e:
            print(f"AI enhancement error: {e}", file=sys.stderr)
            session_data['ai_summary'] = "AI summarization failed"

    def _extract_topics(self, summary: str) -> List[str]:
        """
        Extract key topics from AI summary
        """
        common_topics = [
            'project management', 'ai', 'technology', 
            'development', 'strategy', 'automation'
        ]
        return [
            topic for topic in common_topics 
            if topic.lower() in summary.lower()
        ]

    def _extract_action_items(self, summary: str) -> List[str]:
        """
        Extract action items from AI summary
        """
        # Basic extraction - can be made more sophisticated
        action_markers = ['should', 'need to', 'to do', 'next step', 'action item']
        
        lines = summary.split('\n')
        action_items = [
            line.strip() for line in lines 
            if any(marker in line.lower() for marker in action_markers)
        ]
        
        return action_items

async def main():
    parser = argparse.ArgumentParser(description='SessionTrack Capture CLI')
    parser.add_argument('--source', default='cli', help='Session source')
    parser.add_argument('--project', help='Project name')
    
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
            'timestamp': datetime.now(UTC).isoformat()
        })
    
    # Capture session
    capture = SessionCapture()
    session_file = await capture.capture_session(
        session_key='manual:cli',
        source=args.source,
        messages=messages,
        project=args.project
    )
    
    print(f"Session captured: {session_file}")

if __name__ == '__main__':
    asyncio.run(main())