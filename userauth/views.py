from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .utils import generate_refferal_link
from django.http import JsonResponse
from .models import Sponsor



# metamask account ar madhomme account register and login system and refferal link ar madhomme account register korar code

def metamask_register_login(request):
    ref_code = request.GET.get('ref_code')  # Extract the referral code from the URL

    if request.method == 'POST':
        public_key = request.POST.get('public_key')
        user, created = User.objects.get_or_create(username=public_key)

        if ref_code:
            try:
                sponsor = Sponsor.objects.get(code=ref_code)
                user.sponsor.recommended_by = sponsor.user
                user.sponsor.save()
            except Sponsor.DoesNotExist:
                pass  # Handle the case when the referral code is not found

        login(request, user)
        messages.success(request, f'Logged in successfully! {user}')
        return redirect('homepage')  # Redirect to dashboard or any desired page after login

    return render(request, 'metamask.html')





# account logout system ar code 

def logout_view(request):
    user = request.user
    user.save()
    logout(request)
    messages.success(request, ' successfully logged out.')
    return redirect('homepage')


# my profile page
@login_required
def ProfileView(request):
    return render(request, 'profile.html')




# refferal code and refferal link create koralm
def ReffaralLinkView(request):
    refferal_code = Sponsor.objects.filter(user=request.user)
    user = request.user
    sponsor_code = None
    if user.is_authenticated:
        sponsor_code = user.sponsor.code if hasattr(user, 'sponsor') else None
    refferal_link = generate_refferal_link(request, user, sponsor_code)
    return render(request, 'Deshboard/refferal2.html', {'refferal_code': refferal_code, 'refferal_link': refferal_link})



def main_view(request, *args, **kwargs):
    
    code = str(kwargs.get('ref_code'))
    try:
        profile = Sponsor.objects.get(code = code)
        request.session['ref_profile'] = profile.id
        print('id', profile.id)
        
    except:
        pass
    print(request.session.get_expiry_date())  
    return render(request,'main.html', )




    

