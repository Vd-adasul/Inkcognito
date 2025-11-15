"""
Fast content generation module.
Generates 2000-3000 word passages using Gemini API.
"""
import google.generativeai as genai
from config.config import GEMINI_API_KEY, GEMINI_MODEL


class ContentGenerator:
    """Fast content generator using Gemini API."""
    
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        self.gem = genai.GenerativeModel(GEMINI_MODEL)
    
    def generate(self, prompt):
        """
        Generate 2000-3000 word content from a prompt.
        
        Args:
            prompt (str): The input prompt for content generation
            
        Returns:
            str: Generated content (2000-3000 words)
        """
        print("Generating content...")
        
        # Single API call with clear instructions for 2000-3000 words
        system_prompt = """You are an expert writer. Write a comprehensive, well-structured article that is between 2000-3000 words in length.

Requirements:
- Write exactly 2000-3000 words (aim for the middle range around 2500 words)
- Use a natural, engaging writing style
- Ensure the content is well-structured with clear sections
- Make it informative and detailed
- Use smooth transitions between paragraphs
- Write in a human-like, conversational tone

Now write the article based on the following prompt:"""
        
        full_prompt = f"{system_prompt}\n\n{prompt}"
        
        # Generate content
        response = self.gem.generate_content(full_prompt)
        generated_text = getattr(response, "text", str(response))
        
        print("Generation complete!")
        return generated_text
