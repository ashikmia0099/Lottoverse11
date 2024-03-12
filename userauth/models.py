from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from . utils import generate_ref_code
 
class Sponsor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    code = models.CharField(max_length = 12, blank = True)
    recommended_by = models.ForeignKey(User, on_delete = models.CASCADE, blank= True, null =True, related_name = 'ref_by',)
    
    class Meta: 
        verbose_name = 'Sponsor'
        
    def __str__(self):
        return f"{self.user.username} - gennerated code :  {self.code}, Recommended By: {self.recommended_by} "
        
    def get_recommended_profiles(self):
        recommended_profiles = Sponsor.objects.filter(recommended_by=self.user)
        recommended_profiles_info = []

        for profile in recommended_profiles:
            recommended_profiles_info.append({
                'username': profile.user.username,
                'recommended_by': profile.recommended_by.username if profile.recommended_by else None
            })

        return recommended_profiles_info 
        
        
    def save(self, *args , **kwargs):
    
        if self.code == '':
            code = generate_ref_code()
            self.code = code
            
        super().save(*args, **kwargs)

    def registster_link(self):
        return reverse('registerpage') + f'?ref_code={self.code}'
    
    
    
    
    
    
    
    