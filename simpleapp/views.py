from django.shortcuts import render,redirect
from package.models import Package,ShoppingCard,PurchesHistory
from wallet.models import AccountBalance,Transaction
from django.contrib import messages
from decimal import Decimal

def Payment(request):
    
    if request.method == 'POST':
        
        total_price = request.POST.get('total_price')
        user = request.user
        balance = user.balance
    
        if balance.balance >= Decimal(total_price) :
            user.balance.balance -= Decimal(total_price)
            user.balance.save()
             
            shopping_data = ShoppingCard.objects.filter(user = user)
            
            for item in shopping_data:
                PurchesHistory.objects.create(
                    
                    user = user,
                    package = item.package,
                    ticket_number = item.ticket_number,
                    ticket_price = item.ticket_price
                )
                item.delete()        

            messages.success(request,'Payment Successfully')
        
        else:
            messages.error(request, 'Insufficient balance')
            
            
    shopping_data = ShoppingCard.objects.filter(user = user)
    total_price = sum(item.ticket_price for item in shopping_data)
        
    return render(request, 'Package/shopping_card.html', {'shopping_data': shopping_data, 'total_price': total_price})



def ShoppingHistory(request):
    user = request.user
    data = PurchesHistory.objects.filter(user = user)
    
    return render(request,'Deshboard/viewticket.html', {'data': data})
