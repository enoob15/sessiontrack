#!/usr/bin/env python3
import os
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Union

class TokenManager:
    """
    Manages token consumption and provides intelligent AI processing strategies
    """
    TOKEN_COSTS = {
        'input': 0.00005,  # $0.00005 per input token
        'output': 0.0002,  # $0.0002 per output token
    }
    
    INSIGHT_LEVELS = {
        'minimal': 0.1,     # Lightweight summary
        'standard': 0.5,    # Balanced insights
        'comprehensive': 1.0  # Full detailed analysis
    }
    
    def __init__(self, monthly_budget: float = 50.00):
        """
        Initialize token manager with monthly budget
        
        Args:
            monthly_budget: Maximum monthly spend on AI processing
        """
        self.monthly_budget = monthly_budget
        self.current_month_spend = 0.0
        self.token_cache = {}
    
    def calculate_token_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost of token processing
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
        
        Returns:
            Total processing cost
        """
        input_cost = input_tokens * self.TOKEN_COSTS['input']
        output_cost = output_tokens * self.TOKEN_COSTS['output']
        return input_cost + output_cost
    
    def can_process(self, input_tokens: int, output_tokens: int) -> bool:
        """
        Determine if processing is allowed based on budget
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
        
        Returns:
            Boolean indicating if processing is allowed
        """
        potential_cost = self.calculate_token_cost(input_tokens, output_tokens)
        return (self.current_month_spend + potential_cost) <= self.monthly_budget
    
    def record_token_usage(self, input_tokens: int, output_tokens: int):
        """
        Record token usage and update monthly spend
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
        """
        self.current_month_spend += self.calculate_token_cost(input_tokens, output_tokens)

class AIInsightGenerator:
    """
    Generates AI-powered insights with intelligent token management
    """
    def __init__(self, token_manager: TokenManager, ai_model=None):
        """
        Initialize AI Insight Generator
        
        Args:
            token_manager: TokenManager instance
            ai_model: AI model for generating insights (optional)
        """
        self.token_manager = token_manager
        self.ai_model = ai_model
    
    async def generate_insights(
        self, 
        conversation: str, 
        insight_level: str = 'standard'
    ) -> Dict[str, Union[str, List[str]]]:
        """
        Generate AI insights with token-aware processing
        
        Args:
            conversation: Full conversation text
            insight_level: Depth of insight generation
        
        Returns:
            Dictionary of AI-generated insights
        """
        # Estimate tokens (rough approximation)
        input_tokens = len(conversation.split()) * 1.3  # Average token estimation
        
        # Check budget and processing capability
        if not self.token_manager.can_process(input_tokens, 500):
            return {
                'summary': 'AI processing skipped due to token budget constraints',
                'topics': [],
                'action_items': []
            }
        
        # If AI model is available, generate insights
        if self.ai_model:
            try:
                # Adjust prompt based on insight level
                insight_config = {
                    'minimal': "Provide a very brief, high-level summary.",
                    'standard': "Provide a balanced summary with key points.",
                    'comprehensive': "Provide a detailed, in-depth analysis."
                }
                
                prompt = f"{insight_config.get(insight_level, insight_config['standard'])}\n\nConversation:\n{conversation}"
                
                # Generate AI response
                response = await self.ai_model.generate_content_async(prompt)
                
                # Record token usage
                self.token_manager.record_token_usage(input_tokens, len(response.text.split()) * 1.3)
                
                return {
                    'summary': response.text,
                    'topics': self._extract_topics(response.text),
                    'action_items': self._extract_action_items(response.text)
                }
            
            except Exception as e:
                return {
                    'summary': f'AI processing error: {str(e)}',
                    'topics': [],
                    'action_items': []
                }
        
        return {
            'summary': 'No AI model configured',
            'topics': [],
            'action_items': []
        }
    
    def _extract_topics(self, text: str) -> List[str]:
        """
        Extract key topics from AI-generated text
        
        Args:
            text: AI-generated text
        
        Returns:
            List of extracted topics
        """
        common_topics = [
            'project management', 'ai', 'technology', 
            'development', 'strategy', 'automation'
        ]
        return [
            topic for topic in common_topics 
            if topic.lower() in text.lower()
        ]
    
    def _extract_action_items(self, text: str) -> List[str]:
        """
        Extract action items from AI-generated text
        
        Args:
            text: AI-generated text
        
        Returns:
            List of extracted action items
        """
        action_markers = ['should', 'need to', 'to do', 'next step', 'action item']
        
        lines = text.split('\n')
        return [
            line.strip() for line in lines 
            if any(marker in line.lower() for marker in action_markers)
        ]

class SessionCapture:
    """
    Captures and processes conversation sessions with AI insights
    """
    def __init__(
        self, 
        base_path: str = '/root/clawd/sessions_archive',
        monthly_ai_budget: float = 50.00
    ):
        """
        Initialize SessionCapture
        
        Args:
            base_path: Directory to store session files
            monthly_ai_budget: Monthly budget for AI processing
        """
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
        
        # Initialize token manager
        self.token_manager = TokenManager(monthly_ai_budget)
        
        # Initialize AI model (placeholder)
        self.ai_insight_generator = AIInsightGenerator(
            token_manager=self.token_manager
        )
    
    async def capture_session(
        self, 
        messages: List[Dict], 
        session_key: Optional[str] = None,
        project: Optional[str] = None,
        insight_level: str = 'standard'
    ) -> Dict:
        """
        Capture a conversation session with optional AI insights
        
        Args:
            messages: List of conversation messages
            session_key: Unique session identifier
            project: Associated project
            insight_level: Depth of AI insights
        
        Returns:
            Captured session data
        """
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Prepare conversation text for AI processing
        conversation_text = "\n".join([
            f"{msg.get('author', 'Unknown')}: {msg.get('content', '')}" 
            for msg in messages
        ])
        
        # Generate AI insights
        ai_insights = await self.ai_insight_generator.generate_insights(
            conversation_text, 
            insight_level
        )
        
        # Prepare session data
        session_data = {
            'id': session_id,
            'session_key': session_key or 'unnamed',
            'timestamp': timestamp,
            'project': project,
            'total_messages': len(messages),
            'participants': list(set(msg.get('author', 'unknown') for msg in messages)),
            'messages': messages,
            'ai_insights': ai_insights
        }
        
        # Save session file
        filename = f"{timestamp}_{session_id}.json"
        filepath = os.path.join(self.base_path, filename)
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        return session_data

def main():
    """
    Example usage of SessionCapture
    """
    import asyncio
    
    async def example():
        capture = SessionCapture(monthly_ai_budget=25.00)
        
        sample_messages = [
            {'author': 'Boone', 'content': 'Let\'s discuss the SessionTrack project'},
            {'author': 'TARS', 'content': 'Great! I have some ideas about AI insights'}
        ]
        
        session = await capture.capture_session(
            messages=sample_messages, 
            project='SessionTrack', 
            insight_level='standard'
        )
        
        print(json.dumps(session, indent=2))
    
    asyncio.run(example())

if __name__ == "__main__":
    main()