"""
Kelly Poem Generator
"""
from groq import Groq
from .config import KELLY_SYSTEM_PROMPT
from .utils import extract_topics


class KellyPoetGenerator:
    """Generate Kelly's skeptical AI poems using Groq API"""
    
    def __init__(self, api_key: str):
        """
        Initialize the poem generator
        
        Args:
            api_key: Groq API key
        """
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
    
    def generate_poem(self, user_question: str, extra_principles: list = None) -> str:
        """
        Generate Kelly's poetic response
        
        Args:
            user_question: User's question about AI
            extra_principles: Optional additional guiding principles
            
        Returns:
            Generated poem as string
        """
        try:
            # Extract topics for context
            topics = extract_topics(user_question)
            topic_context = f"Key topics detected: {', '.join(topics[:3])}" if topics else ""
            
            # Build principles text
            principles_text = "\n".join(extra_principles) if extra_principles else ""
            
            # Construct user message
            user_message = f"{principles_text}\n\n{topic_context}\n\nUser's question: {user_question}\n\nRespond with a skeptical, analytical poem that questions AI claims and provides practical guidance."
            
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": KELLY_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=2048,
            )
            
            # Extract and return the poem
            poem = chat_completion.choices[0].message.content.strip()
            return poem
            
        except Exception as e:
            # Fallback error poem
            return self._generate_error_poem(e)
    
    def _generate_error_poem(self, error: Exception) -> str:
        """Generate error message as a poem"""
        return f"""Kelly encounters an error in the digital mist,
The API stumbles, connections twisted and missed.
{str(error)[:100]}

→ Check your API key and internet connection.
→ Verify Groq API quotas and permissions.
→ Review error logs for deeper inspection."""
