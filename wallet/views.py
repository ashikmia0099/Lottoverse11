from django.shortcuts import render,redirect
from .models import AccountBalance, Transaction
from .forms import TransferForm, DepositeForm
from django.contrib.auth.models import User
from django.contrib import messages

# def Depositeview(request):
#     user_account = request.user.username  # Get the AccountBalance object associated with the current user
#     print(user_account)
    
#     if request.method == 'POST':
#         form = DepositeForm(request.POST)
        
#         if form.is_valid():
            
#             deposite_amount = form.cleaned_data['amount']
#             user_account.balance += deposite_amount
#             user_account.save()
#             print(user_account.balance)
            
#             messages.success(request, f'Deposit successfully {deposite_amount}. Total balance: {user_account.balance}')
            
#             return redirect('deposite_balance')
#     else:
#         form = DepositeForm()
        
#     return render(request, 'deposite.html', {'form': form})




def Depositeview(request):
    current_user = request.user
    
    try:
        user_account = AccountBalance.objects.get(user = current_user)
        
    except AccountBalance.DoesNotExist :
        user_account = AccountBalance.objects.create(user = current_user)
    
    
    if request.method == 'POST':
        form = DepositeForm(request.POST)
        
        if form.is_valid():
            deposite_amount = form.cleaned_data['amount']
            user_account.balance += deposite_amount
            user_account.save()
            
            messages.success(request, f'Deposit successful: {deposite_amount}. Total balance: {user_account.balance}')
            
            return redirect('deposite_balance')
    else:
        form = DepositeForm()
        
    return render(request, 'deposite.html', {'form': form})

def Balanceview(request):
    if request.user.is_authenticated:
        account_balance = request.user.balance  # Retrieve the account balance for the authenticated user
    else:
        account_balance = None  # Set to None for non-authenticated users
        
    return render(request, 'balance.html', {'account_balance': account_balance})



def MyEarning(request):
    
    return render(request,'Deshboard/myearning.html')
