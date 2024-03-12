from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone


class Package(models.Model):
    name = models.CharField(max_length = 20)
    price = models.PositiveIntegerField()
    quentity = models.PositiveIntegerField()
    ticket_numbers = models.JSONField(default=list, blank = True)
    initial_quentity = models.PositiveIntegerField()
    new_package_created = models.BooleanField(default=False)
    
    

    class Meta:
        verbose_name = 'Package'
 
    
    def __str__(self):
        return f"{self.name}"    
    
    


# autometic akti new Package create kora holo 

@receiver(post_save, sender=Package)

def create_new_package(sender, instance, created, **kwargs):
    
    if not created and instance.quentity == 0 and not instance.new_package_created:
        previous_package = Package.objects.filter(name = instance.name).order_by('-id').first()
        
        if previous_package:
            
            Package.objects.create(
                name = previous_package.name,
                price = previous_package.price,
                quentity = previous_package.initial_quentity,
                initial_quentity = previous_package.initial_quentity
            )
            instance.new_package_created = True
            instance.save()
   
        
        
class ShoppingCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='card')
    package = models.ForeignKey(Package, on_delete = models.CASCADE, related_name = 'package')
    ticket_number = models.CharField(max_length = 50)
    ticket_price =models.DecimalField(max_digits = 10, decimal_places = 2)
    total_price =models.DecimalField(max_digits = 10, decimal_places = 2 , default = 0)
    last_ticket_date = models.DateTimeField(default = timezone.now)
    
    
    
    def __str__(self):
        return f' Package: {self.package.name}  Ticket Number {self.ticket_number}, Price: {self.ticket_price}'
        
        
    
    
    
    
        
class PurchesHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purches')
    package = models.ForeignKey(Package, on_delete = models.CASCADE, related_name = 'purchesPackage')
    ticket_number = models.CharField(max_length = 50)
    ticket_price =models.DecimalField(max_digits = 10, decimal_places = 2)  
    purches_date = models.DateTimeField(default = timezone.now)
   
   
    def __str__(self):
        return f' Package: {self.package.name}  Ticket Number {self.ticket_number}, Price: {self.ticket_price}'
        
        
        
class TotalPrice(models.Model):
    package = models.ForeignKey(Package, on_delete = models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    
class Ticket(models.Model):
    ticket_packge = models.ForeignKey(Package, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    ticket_number = models.IntegerField()


# total ticket ar price save ar jonno model

class TicketBalance(models.Model):
    balance = models.DecimalField(max_digits = 18, decimal_places = 2, default = 0)
    
    def __str__(self) -> str:
        return f'Ticket Balance: {self.balance}'

