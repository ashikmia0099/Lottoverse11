from django.db import models
from django.contrib.auth.models import User


class AccountBalance(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'balance')
    balance = models.DecimalField(default = 0, max_digits = 12, decimal_places = 2)
    
    
    class Meta:
        verbose_name = 'AccountBalance'
        verbose_name_plural = 'AccountBalance'
        
    def __str__(self):
        return f" User_Address: {self.user.username} - Balance : {self.balance}" 
    
    
    

    
    
class Transaction(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'transaction')
    transferUser = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'transferuser')
    amount = models.DecimalField(default = 0, max_digits = 12, decimal_places = 2)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transaction'
        
    def __str__(self):
        return f"Transferd Form : {self.user} - Transfer To : {self.transferUser}"
    
    
    
    