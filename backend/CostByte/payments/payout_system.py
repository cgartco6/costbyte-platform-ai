"""
Weekly payout system with percentage distribution
"""
import asyncio
from datetime import datetime, timedelta
from django.conf import settings
from .models import Revenue, Payout
from .payment_processors.eft_processor import EFTProcessor

class WeeklyPayoutSystem:
    """Handle weekly revenue distribution"""
    
    def __init__(self):
        self.eft_processor = EFTProcessor()
        self.payout_config = {
            'encore_aspire': {'account': settings.ENCORE_ASPIRE_ACCOUNT, 'percentage': 0.40},
            'my_world_african': {'account': settings.MY_WORLD_AFRICAN_ACCOUNT, 'percentage': 0.15},
            'nexus_platform': {'account': settings.NEXUS_PLATFORM_ACCOUNT, 'percentage': 0.20},
            'apex_digital': {'account': settings.APEX_DIGITAL_ACCOUNT, 'percentage': 0.20},
        }
    
    async def process_weekly_payouts(self):
        """Process weekly payouts every Monday"""
        # Calculate weekly revenue
        start_date = datetime.now() - timedelta(days=7)
        weekly_revenue = Revenue.objects.filter(
            created_at__gte=start_date,
            payout_processed=False
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        if weekly_revenue <= 0:
            return
        
        # Process payouts to each account
        payouts = []
        for account_name, config in self.payout_config.items():
            amount = weekly_revenue * config['percentage']
            
            payout = await self.eft_processor.transfer(
                amount=amount,
                from_account=settings.FNB_BUSINESS_ZERO_ACCOUNT,
                to_account=config['account'],
                reference=f"WEEKLY_PAYOUT_{datetime.now().strftime('%Y%W')}_{account_name.upper()}"
            )
            
            # Record payout
            payout_record = Payout.objects.create(
                account_name=account_name,
                amount=amount,
                percentage=config['percentage'],
                status=payout.status,
                transaction_id=payout.transaction_id
            )
            payouts.append(payout_record)
        
        # Mark revenue as processed
        Revenue.objects.filter(
            created_at__gte=start_date,
            payout_processed=False
        ).update(payout_processed=True)
        
        return payouts
    
    async def schedule_weekly_payouts(self):
        """Schedule automatic weekly payouts"""
        while True:
            now = datetime.now()
            # Run every Monday at 9 AM
            next_monday = now + timedelta(days=(7 - now.weekday()))
            next_run = next_monday.replace(hour=9, minute=0, second=0, microsecond=0)
            
            sleep_seconds = (next_run - now).total_seconds()
            await asyncio.sleep(sleep_seconds)
            
            await self.process_weekly_payouts()
