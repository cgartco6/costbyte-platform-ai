"""
Automated job application system
"""
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from ..models import JobListing, JobApplication, User

class JobApplicationBot:
    """Automatically apply to jobs users qualify for"""
    
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Selenium WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
    
    async def auto_apply_for_user(self, user_id):
        """Automatically apply to qualified jobs for user"""
        user = User.objects.get(id=user_id)
        user_resume = user.resumes.filter(is_available=True).first()
        
        if not user_resume:
            return
        
        # Get qualified job listings
        qualified_jobs = await self.find_qualified_jobs(user)
        
        applications = []
        for job in qualified_jobs:
            application = await self.apply_to_job(job, user, user_resume)
            applications.append(application)
            
            # Rate limiting
            await asyncio.sleep(2)
        
        return applications
    
    async def find_qualified_jobs(self, user):
        """Find jobs user qualifies for based on resume and qualifications"""
        # Use AI matching algorithm
        from ..ai_models.model_trainer import ModelTrainer
        model_trainer = ModelTrainer()
        
        user_profile = await self.extract_user_profile(user)
        recent_jobs = JobListing.objects.filter(
            is_active=True,
            posted_date__gte=datetime.now() - timedelta(days=30)
        )
        
        qualified_jobs = []
        for job in recent_jobs:
            match_score = await model_trainer.calculate_job_match(
                user_profile, 
                job.description
            )
            
            if match_score >= settings.MIN_MATCH_THRESHOLD:
                qualified_jobs.append(job)
        
        return qualified_jobs
    
    async def apply_to_job(self, job, user, resume):
        """Apply to a specific job"""
        try:
            self.driver.get(job.apply_url)
            
            # Fill application form
            await self.fill_application_form(user, resume, job)
            
            # Submit application
            submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
            submit_button.click()
            
            # Record application
            application = JobApplication.objects.create(
                user=user,
                job=job,
                resume_used=resume,
                status='submitted',
                applied_at=datetime.now()
            )
            
            return application
            
        except Exception as e:
            print(f"Failed to apply to job {job.id}: {str(e)}")
            return None
