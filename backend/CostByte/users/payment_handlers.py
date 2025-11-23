"""
Payment processing for user registration (R500)
"""
from django.conf import settings
from .models import User, Payment
from ..payments.payment_processors import (
    EFTProcessor, 
    PayFastProcessor, 
    PayShapProcessor
)

class RegistrationPaymentHandler:
    """Handle R500 registration payments"""
    
    def __init__(self):
        self.eft_processor = EFTProcessor()
        self.payfast_processor = PayFastProcessor()
        self.payshap_processor = PayShapProcessor()
        self.fnb_account = settings.FNB_BUSINESS_ZERO_ACCOUNT
    
    async def process_registration_payment(self, user_id, payment_method, amount=500):
        """Process R500 registration payment"""
        user = User.objects.get(id=user_id)
        
        if payment_method == 'eft':
            result = await self.eft_processor.process_payment(
                amount=amount,
                account=self.fnb_account,
                reference=f"REG_{user.id}"
            )
        elif payment_method == 'payfast':
            result = await self.payfast_processor.process_payment(
                amount=amount,
                buyer=user,
                return_url=settings.PAYMENT_RETURN_URL
            )
        elif payment_method == 'payshap':
            result = await self.payshap_processor.process_payment(
                amount=amount,
                recipient=self.fnb_account,
                reference=f"REG_{user.id}"
            )
        else:
            raise ValueError("Unsupported payment method")
        
        # Create payment record
        payment = Payment.objects.create(
            user=user,
            amount=amount,
            payment_method=payment_method,
            status=result.status,
            transaction_id=result.transaction_id
        )
        
        if result.success:
            await self.activate_user_account(user)
        
        return payment
    
    async def activate_user_account(self, user):
        """Activate user account after successful payment"""
        user.is_active = True
        user.payment_status = 'paid'
        user.save()
        
        # Trigger resume processing
        await self.process_user_documents(user)
