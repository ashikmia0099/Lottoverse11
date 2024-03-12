import os
import string
import time
import random
from random import randint
from decimal import Decimal
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Package,ShoppingCard,PurchesHistory, Ticket,TotalPrice
from django.contrib import messages
from django.urls import reverse
from django.db.models import F, Sum
from django.http import HttpResponseRedirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from web3 import HTTPProvider, Web3
from django.http import JsonResponse
from wallet.models import AccountBalance, Transaction



# Random number Ticket Generate Code 




# # add ticket      

def AddPackage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quentity = request.POST.get('quentity')
        tickets = generate_tickets(int(quentity))
        
        
        pack = Package.objects.create(name=name, price=price, quentity=quentity, ticket_number = tickets)
        
        
        
    packages = Package.objects.all()
    
    context = {
        'packages': packages
    }
    return render(request, 'Package/ticketcard.html', context)






# Random number Ticket Generate Code 

class CustomBaseEncoder:
    def __init__(self):
        self.characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        self.base = len(self.characters)

    def encode(self, byte_data):
        number = int.from_bytes(byte_data, byteorder='big')
        result = ""
        while number:
            number, i = divmod(number, self.base)
            result = self.characters[i] + result
        return result

def generate_tickets(package):
    encoder = CustomBaseEncoder()
    tickets = []
    for _ in range(package.quentity):
        num = (round((time.time_ns()) // 10 ** 10)) + int(time.time() * 1000)
        num_bytes = num.to_bytes((num.bit_length() + 7) // 8, 'big')
        random_bytes = os.urandom(1)
        combined_bytes = num_bytes + random_bytes
        ticket_number = encoder.encode(combined_bytes)
        tickets.append(ticket_number)

    package.ticket_numbers = tickets
    package.save()

    return tickets




# sobgolo package ar all ticket show korar code

def ticket_view(request):
    
    packages = Package.objects.filter(quentity__gt = 0)
    tickets_by_package = {}
    
    for package in packages:
        
        if not package.ticket_numbers:
            generate_tickets(package)
            
        tickets_by_package[package] = package.ticket_numbers
        
        
    card_items = ShoppingCard.objects.all()
    total_price = sum(item.ticket_price for item in card_items)
    
    
    return render(request, 'Deshboard/randomticket.html', {'tickets_by_package': tickets_by_package, 'card': card_items, 'total_price': total_price})




# randomly ticket number card a add hocce akane maximum 10 ti ticket number select hocce

def add_to_card(request):
    
    # deactivate_inactive_users function ka call kora hoice
    
    deactivate_inactive_users()
    
    all_packages = Package.objects.all()
    
    total_tickets_available = sum(package.quentity for package in all_packages)
    
    if total_tickets_available <= 2:
        return redirect(reverse('packagepage'))  
    
    max_tickets = min(1, total_tickets_available)
    selected_tickets = []
    
    for package in all_packages:
        
        max_tickets_from_package = min(package.quentity, max_tickets - len(selected_tickets))
        
        
       
        if max_tickets_from_package == 0:
            break
        
        num_tickets = randint(1, max_tickets_from_package)
            
        
        num_tickets = randint(1, max_tickets_from_package)
        
        # Ensure to select tickets randomly from package.ticket_numbers
        tickets = random.sample(package.ticket_numbers, num_tickets)
        
        package.ticket_numbers = list(set(package.ticket_numbers) - set(tickets))
       
        package.quentity -= num_tickets
        package.save()
        
        for ticket_number in tickets:
            ticket_price = package.price
            selected_tickets.append({
                'package': package,
                'ticket_number': ticket_number,
                'ticket_price': ticket_price
            })
    
    
    user = request.user
    for ticket_info in selected_tickets:
        ShoppingCard.objects.create(
            user=user,
            package=ticket_info['package'], 
            ticket_number=ticket_info['ticket_number'],
            ticket_price=ticket_info['ticket_price']
        )
        
        # ticket kinar pro user ke active korar jonno code 
        
        if not user.is_active :
            
            user.is_active = True
            user.save()
        
        
    return redirect(reverse('packagepage'))





# Akti kore ticket select korar view 


def select_ticket (request, package_id=None, ticket_number=None):
    
    deactivate_inactive_users()
    
    if package_id and ticket_number:
        try:
            package = Package.objects.get(pk=package_id)
            
            if ticket_number in package.ticket_numbers:
                encoder = CustomBaseEncoder()
            
                ShoppingCard.objects.create(
                    user=request.user,
                    package=package,
                    ticket_number=ticket_number,
                    ticket_price=package.price
                )
                
                
                
                package.ticket_numbers.remove(ticket_number)
                package.save()
                package.quentity -= 1
                package.save()
                
                
            
            
        except Package.DoesNotExist:
            return redirect(reverse('packagepage'))
        
     # ticket kinar pro user ke active korar jonno code     
    
    if not request.user.is_active:
        request.user.is_active = True
        request.user.save()
    

    return HttpResponseRedirect(reverse('packagepage'))





# ja ticket golo card select kora hoice tar view list code 

def shopping_card_view(request):
    # Retrieve shopping card items for the current user
    user = request.user
    shopping_data = ShoppingCard.objects.filter(user=user)
    
    total_price = ShoppingCard.objects.filter(user=user).aggregate(total_price=Sum('ticket_price'))['total_price'] or 0
    

    
    return render(request, 'Package/shopping_card.html', {'shopping_data': shopping_data, 'total_price': total_price})





# Card ar ticket remove korar code 

def cancel_ticket(request, id):
    try:
        item = ShoppingCard.objects.get(pk=id)
        # Retrieve the package associated with the ticket
        package = item.package
        
        # Subtract ticket price from total price
        user = request.user
        shopping_card_items = ShoppingCard.objects.filter(user=user)
        total_price = sum(item.ticket_price for item in shopping_card_items) - item.ticket_price
        
        # Update total price in the ShoppingCard model
        ShoppingCard.objects.filter(user=user).update(total_price=total_price)
        
        # Add the ticket price back to the package availability
        Package.objects.filter(pk=package.pk).update(quentity=F('quentity') + 1)
        
        # Delete the ticket from the shopping card
        item.delete()
        
        return redirect(reverse('shoppingcardpage'))
    except ShoppingCard.DoesNotExist:
        # Handle if the shopping card item doesn't exist
        return redirect(reverse('shoppingcardpage'))


# user deactive korat jonno ai function kora hoice 

def deactivate_inactive_users():

    thirty_days_ago = timezone.now() - timedelta(days= 30)
    inactive_users = ShoppingCard.objects.filter(last_ticket_date__lt=thirty_days_ago, user__is_active=True).values('user').distinct()

    
    for user_data in inactive_users :
        user = User.objects.get(pk = user_data ['user'])
        user.is_active = False
        user.save()





def ShoppingHistory(request):
    
    return render(request,'Deshboard/viewticket.html')


# Use this method, web3.is_connected()

# Define the function to deduct balance from user's Ethereum account
def deduct_balance_from_ethereum_account(request,ethereum_account, total_price):
    
    # Get the sender address from the authenticated user
    sender_address = request.user.username  # Replace 'ethereum_address' with the actual field name in your User model
    
    ethereum_account = Web3.is_checksum_address(ethereum_account)
    
    # Check if the Ethereum node is connected
    if web3.is_connected():
        # Check if the Ethereum account exists
        if web3.is_address(ethereum_account):
            # Get the balance of the Ethereum account
            balance = web3.eth.get_balance(ethereum_account)
            
            # Convert balance from wei to ether (1 ether = 10^18 wei)
            balance_in_ether = web3.from_wei(balance, 'ether')
            total_price_decimal = Decimal(total_price)
            
            
            # Check if the account has sufficient balance
            if balance_in_ether >= total_price_decimal:
                # Calculate the amount to deduct (convert total_price to wei)
                amount_to_deduct = web3.to_wei(total_price_decimal, 'ether')
                
                # Send a transaction to deduct the balance
                # This is a basic example, you should handle errors and gas properly in a real-world scenario
                tx_hash = web3.eth.send_transaction({
                    'from': sender_address,
                    'to': ethereum_account,
                    'value': amount_to_deduct
                })
                
                # Wait for the transaction to be mined
                web3.eth.wait_for_transaction_receipt(tx_hash)
                
                # Return True indicating successful deduction
                return True
            else:
                # Insufficient balance, return False
                return False
        else:
            # Invalid Ethereum account, return False
            return False
    else:
        # Ethereum node not connected, return False
        return False


web3 = Web3(HTTPProvider('http://127.0.0.1:7545'))  # Replace with your Ethereum node's RPC endpoint

def handle_payment(request, total_price):
    user = request.user
    
    # Get the Ethereum account number (in this case, using the username)
    ethereum_account = user.username
    
    try:
        # Check connection status by attempting to get the current block number
        current_block_number = web3.eth.block_number
        
        # If the above line executes without error, it means there is a connection
        # Proceed with payment logic
        if deduct_balance_from_ethereum_account(request,ethereum_account, total_price):
            # Transfer shopping card data to shopping history
            shopping_card_items = ShoppingCard.objects.filter(user = user)
            
            for item in shopping_card_items:
                PurchesHistory.objects.create(
                    user=user,
                    package=item.package,
                    ticket_number=item.ticket_number,
                    ticket_price=item.ticket_price,
                    purches_date=item.last_ticket_date
                    
                )
                # Clear shopping card for the user
                item.delete()
            
            messages.success(request, "Payment successful. Your shopping card data has been transferred to history.")
            return redirect('shoppinghistorypage')  # Redirect to history page
        else:
            messages.error(request, "Payment failed: Insufficient balance or Ethereum network error.")
            return redirect('shoppingcardpage')  # Redirect to shopping card page with error message
    except Exception as e:
        messages.error(request, f"Payment failed: {str(e)}")
        return redirect('shoppingcardpage')  # Redirect to shopping card page with error message



def history(request):
    user = request.user
    shopping_history = ShoppingHistory.objects.filter(user=user)
    return render(request, 'history.html', {'shopping_history': shopping_history})



# kon kon user ticket purches korce tadar username code 


def userShoppingCard(request):
    
    shopping_data = PurchesHistory.objects.all().select_related('user', 'package')
    
    return render(request,'userShoppingCard.html',{'shopping_data': shopping_data})





# winner set korar jonno 

def SelectWinner(package_id):
    package = Package.objects.get(id= package_id)
    
    if package.quentity == 0:
        tickets = Ticket.objects.filter(package= package)
        winners = random.simple(list(tickets), min(len(tickets), 5))
        total_prize = TotalPrice.total_price
        first_prize = total_prize * .25
        second_prize = total_prize *.15
        remaining_prize = total_prize - first_prize - second_prize - (10*(len(winners) - 2))
        
        for i, winner in enumerate(winners):
            
            account_balance, _ = AccountBalance.objects.get_or_create(user= winner.user)
            
            
            if i == 0:
                account_balance.balance += first_prize
                
            elif i == 1:
                account_balance.balance += second_prize
                
            else:
                account_balance.balance += 10
                
            account_balance.save()
        
        superuser_balance, _ = AccountBalance.objects.get_or_create(user = User.objects.get(username = 'superuser'))
        superuser_balance.balance += remaining_prize
        superuser_balance.save()

        for winner in winners:
            Transaction.objects.create(user = winner.user, transferUser= None, amount = first_prize)
        
        Transaction.objects.create(user = User.objects.get(username = 'superuser', transferUser= None, amount= remaining_prize))

        package.quentity = 10
        package.save()
