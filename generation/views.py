from django.shortcuts import render,redirect
from decimal import Decimal
from itertools import zip_longest
from package.models import Package,ShoppingCard
from userauth.models import Sponsor
from django.contrib.auth.models import User

# Generations structures code 

def structure (request):
    
    user = request.user
    generations = 7
    all_gen_users = []

    for gen in range(1, generations + 1):
        refer_gen = Sponsor.objects.filter(recommended_by=user)
        for _ in range(gen - 1):
            refer_gen = Sponsor.objects.filter(recommended_by__in=[sponsor.user for sponsor in refer_gen])

        gen_users = User.objects.filter(username__in=[sponsor.user.username for sponsor in refer_gen])
        all_gen_users.append(gen_users)
    

    zipped_data = zip_longest(range(1, generations + 1), all_gen_users)
    

    context = {
        'zipped_data': zipped_data,
        'user': user,
    }
    
    return render (request, 'Deshboard/structure.html',context )





# 7 ta generations show and commitions show 


def GenerationView(request):
    user = request.user
    generations = 7
    
    gen_count = [0] * generations
    gen_active_countes = [0]* generations
    gen_inactive_countes = [0]* generations
    total_commissions = [Decimal(0)]*generations
    
    total_active_refferals = 0 
    total_inactive_refferals = 0 
    total_refferal_commission = Decimal(0)
    
 
    
    commission_percentages = {1: 10, 2: 5, 3: 3, 4: 2, 5: 1, 6: 1, 7: 1}
    
    for gen in range(1, generations + 1):
        refer_gen = Sponsor.objects.filter(recommended_by=user)
        
        for _ in range(gen - 1):
            refer_gen = Sponsor.objects.filter(recommended_by__in=[sponsor.user for sponsor in refer_gen])
        
        
        gen_users = User.objects.filter(username__in=[sponsor.user.username for sponsor in refer_gen])
        gen_count[gen - 1] += len(gen_users)
        
        
        for gen_user in gen_users :
            if gen_user.is_active :
                gen_active_countes[gen - 1] += 1
                total_active_refferals += 1
                
            else:
                gen_active_countes [ gen - 1] += 1
                total_inactive_refferals += 1
                
            # akane ShoppingCard ar ticket ar price divide kora holo    
            
            if gen_user :
                buy_ticket = ShoppingCard.objects.filter (user = gen_user, )
                
                for order in buy_ticket :
                    commission_percentages = Decimal(commission_percentages.get(gen , 0))
                    commission_amount = order.total_price * (commission_percentages / Decimal(100))
                    
                    total_commissions [gen-1] += commission_amount
                    total_refferal_commission += commission_amount
    
    total_referrals = sum(gen_count)
    
    zipped_data = zip_longest (
        range(1, generations + 1),
        gen_count,
        gen_active_countes,
        gen_inactive_countes,
        total_commissions,
    )
    
    context = {
        'zipped_data': zipped_data,
        'total_referrals': total_referrals,
        'total_active_refferals' : total_active_refferals,
        'total_inactive_refferals' : total_inactive_refferals,
        'total_refferal_commission' : total_refferal_commission
    }
    
    return render (request, 'Deshboard/generations.html', context)
        
        
         