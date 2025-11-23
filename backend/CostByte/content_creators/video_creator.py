"""
AI video content creator for marketing
"""
import openai
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

class VideoContentCreator:
    """Create marketing videos, reels, shorts automatically"""
    
    def __init__(self):
        self.openai_client = openai.Client(api_key=settings.OPENAI_API_KEY)
    
    async def create_marketing_video(self, platform, content_type, theme):
        """Create AI-generated marketing video"""
        
        # Generate script
        script = await self.generate_video_script(theme, platform, content_type)
        
        # Generate voiceover
        voiceover_path = await self.generate_voiceover(script)
        
        # Create visuals
        video_path = await self.generate_visuals(script, theme)
        
        # Combine elements
        final_video = await self.combine_video_elements(
            video_path, 
            voiceover_path, 
            script
        )
        
        return final_video
    
    async def generate_video_script(self, theme, platform, content_type):
        """Generate engaging video script using AI"""
        prompt = f"""
        Create a {content_type} video script for {platform} about {theme}.
        Target audience: job seekers in South Africa.
        Tone: motivational, professional, engaging.
        Length: {"15-30 seconds" if content_type in ['reel', 'short'] else "1-2 minutes"}
        Include: hook, value proposition, call-to-action
        """
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        return response.choices[0].message.content
