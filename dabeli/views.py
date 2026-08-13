from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Rating


# Create your views here.
from .models import Contact, Category, MenuItem

from .models import Contact, Category, MenuItem, HomePageContent

def index(request):
    home_content = HomePageContent.objects.first()
    categories = Category.objects.all()
    items = MenuItem.objects.filter(is_available=True)
    return render(request, 'index.html', {'home_content': home_content, 'categories': categories, 'items': items})

def about(request):
    return render(request, 'about.html')

from django.http import JsonResponse

def menu(request):
    categories = Category.objects.all()
    items = MenuItem.objects.filter(is_available=True)
    return render(request, 'menu.html', {'categories': categories, 'items': items})

def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id = str(item_id)
    if item_id in cart:
        cart[item_id] += 1
    else:
        cart[item_id] = 1
    request.session['cart'] = cart
    return JsonResponse({'status': 'success', 'cart_count': sum(cart.values())})

def get_cart_data(request):
    cart = request.session.get('cart', {})
    items = []
    total_items = 0
    for item_id, qty in cart.items():
        try:
            item = MenuItem.objects.get(id=item_id)
            items.append({
                'id': item.id,
                'name': item.name,
                'qty': qty
            })
            total_items += qty
        except MenuItem.DoesNotExist:
            pass
    return JsonResponse({'items': items, 'total_items': total_items})

# def login(request):
#      return render(request, 'login.html')
def rate_us(request):
    return render(request, 'rate_us.html')
def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        category=request.POST.get('category')
        
        contact = Contact(name=name, phone=phone, message=message ,category=category,)
        
        contact.save()
        messages.success(request, "Your message has been sent!")
    return render(request, 'contact.html')

# views.py
def submit_rating(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        rating = request.POST.get('rating')
        comments = request.POST.get('comments')

        Rating.objects.create(
            name=name,
            rating=int(rating),
            comments=comments
        )
        return redirect('thank_you')

    return render(request, 'index.html')

def thank_you(request):
    return render(request, 'thank_you.html')


# def contact_form(request):
#     if request.method == 'post':
#         name=request.POST.get('name')
#         phone=request.POST.get('phone')
#         message=request.POST.get('message')
#         savedetails = contact(name=name , phone=phone, message=message)
#         savedetails.save()
#     return render(request, 'contact.html')
#
# # def contact(request):

# views.py

from django.contrib.auth import authenticate, login

# def signin(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             return redirect('home')  # Replace 'home' with your actual home URL
#         else:
#             # Handle invalid login credentials
#             pass
#
#     return render(request, 'login.html')  # Create a template for the sign-in page
#
