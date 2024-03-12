import uuid
from django.conf import settings



def generate_ref_code():
    
    code = str(uuid.uuid4()).replace('-','')[: 12]

    return code


def generate_refferal_link(request, user, sponsor_code):
    base_url = settings.BASE_URL
    
    if user.is_authenticated:
        if sponsor_code:
            referral_link = f"{base_url}/userauth/metamask/?ref_code={sponsor_code}"
        else:
            referral_link = f"{base_url}/userauth/metamask/"
    else:
        referral_link = f"{base_url}/userauth/metamask/"
    
    return referral_link