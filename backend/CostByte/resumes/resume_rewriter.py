"""
AI-powered resume/CV rewriting system
"""
import openai
from django.conf import settings
from ..ai_models.model_trainer import ModelTrainer
from .models import Resume, UserDocument

class ResumeRewriter:
    """Rewrite and optimize resumes using AI"""
    
    def __init__(self):
        self.model_trainer = ModelTrainer()
        self.openai_client = openai.Client(api_key=settings.OPENAI_API_KEY)
    
    async def rewrite_resume(self, user_id, original_resume_path, photo_path=None):
        """Rewrite user's resume using AI"""
        user = User.objects.get(id=user_id)
        
        # Extract text from resume
        resume_text = await self.extract_resume_text(original_resume_path)
        
        # Analyze resume content
        analysis = await self.analyze_resume(resume_text)
        
        # Generate optimized resume
        optimized_resume = await self.generate_optimized_resume(
            resume_text, 
            analysis,
            user.qualifications
        )
        
        # Create professional format
        formatted_resume = await self.format_resume(optimized_resume, user, photo_path)
        
        # Save new resume
        new_resume = Resume.objects.create(
            user=user,
            original_file=original_resume_path,
            optimized_content=formatted_resume,
            analysis_metadata=analysis,
            is_available=True
        )
        
        return new_resume
    
    async def create_resume_from_scratch(self, user_id, user_data, photo_path=None):
        """Create resume for users without one"""
        user = User.objects.get(id=user_id)
        
        # Generate resume content based on user data
        resume_content = await self.generate_resume_content(user_data)
        
        # Format professionally
        formatted_resume = await self.format_resume(resume_content, user, photo_path)
        
        # Save resume
        new_resume = Resume.objects.create(
            user=user,
            optimized_content=formatted_resume,
            is_available=True,
            generated_from_scratch=True
        )
        
        return new_resume
    
    async def generate_optimized_resume(self, original_text, analysis, qualifications):
        """Use AI to optimize resume content"""
        prompt = f"""
        Optimize this resume for ATS systems and modern hiring practices:
        
        Original Resume: {original_text}
        
        Qualifications: {qualifications}
        
        Analysis: {analysis}
        
        Please create a professional, optimized resume that:
        1. Is ATS-friendly
        2. Highlights key achievements
        3. Uses industry-specific keywords
        4. Has proper formatting
        5. Is 1-2 pages maximum
        """
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        
        return response.choices[0].message.content
