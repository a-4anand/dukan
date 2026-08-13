from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from .models import Contact, Category, MenuItem, HomePageContent, Rating, ShopSettings


def get_shop_settings():
    settings = ShopSettings.objects.first()
    if not settings:
        settings = ShopSettings.objects.create()
    return settings


def index(request):
    home_content = HomePageContent.objects.first()
    categories = Category.objects.all()
    items = MenuItem.objects.filter(is_available=True)
    shop = get_shop_settings()
    return render(request, 'index.html', {
        'home_content': home_content,
        'categories': categories,
        'items': items,
        'shop': shop,
    })


def about(request):
    return render(request, 'about.html')


def menu(request):
    categories = Category.objects.all()
    items = MenuItem.objects.filter(is_available=True)
    shop = get_shop_settings()
    return render(request, 'menu.html', {
        'categories': categories,
        'items': items,
        'shop': shop,
    })


def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id = str(item_id)
    if item_id in cart:
        cart[item_id] += 1
    else:
        cart[item_id] = 1
    request.session['cart'] = cart
    return JsonResponse({'status': 'success', 'cart_count': sum(cart.values())})


def update_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id = str(item_id)
    action = request.GET.get('action', 'add')
    if action == 'add':
        cart[item_id] = cart.get(item_id, 0) + 1
    elif action == 'remove':
        if item_id in cart:
            cart[item_id] -= 1
            if cart[item_id] <= 0:
                del cart[item_id]
    elif action == 'delete':
        cart.pop(item_id, None)
    request.session['cart'] = cart
    return JsonResponse({'status': 'success', 'cart_count': sum(cart.values())})


def get_cart_data(request):
    cart = request.session.get('cart', {})
    shop = get_shop_settings()
    items = []
    subtotal = 0
    total_items = 0
    for item_id, qty in cart.items():
        try:
            item = MenuItem.objects.get(id=item_id)
            item_total = float(item.price) * qty
            items.append({
                'id': item.id,
                'name': item.name,
                'price': float(item.price),
                'qty': qty,
                'item_total': item_total,
            })
            subtotal += item_total
            total_items += qty
        except MenuItem.DoesNotExist:
            pass

    # Calculate delivery
    delivery_charge = float(shop.delivery_charge)
    free_delivery_above = float(shop.free_delivery_above)
    if free_delivery_above > 0 and subtotal >= free_delivery_above:
        delivery_charge = 0

    # Calculate discount
    discount = 0
    discount_pct = float(shop.discount_percentage)
    discount_min = float(shop.discount_min_order)
    if discount_pct > 0 and subtotal >= discount_min:
        discount = round(subtotal * discount_pct / 100, 2)

    grand_total = subtotal + delivery_charge - discount

    return JsonResponse({
        'items': items,
        'total_items': total_items,
        'subtotal': round(subtotal, 2),
        'delivery_charge': round(delivery_charge, 2),
        'free_delivery_above': round(free_delivery_above, 2),
        'discount': round(discount, 2),
        'discount_percentage': discount_pct,
        'grand_total': round(max(grand_total, 0), 2),
        'whatsapp_number': shop.whatsapp_number,
        'is_shop_open': shop.is_shop_open,
        'shop_message': shop.shop_open_message if shop.is_shop_open else shop.shop_closed_message,
    })


def rate_us(request):
    return render(request, 'rate_us.html')


def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        category = request.POST.get('category')
        contact = Contact(name=name, phone=phone, message=message, category=category)
        contact.save()
        messages.success(request, "Your message has been sent!")
    return render(request, 'contact.html')


def submit_rating(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        rating = request.POST.get('rating')
        comments = request.POST.get('comments')
        Rating.objects.create(name=name, rating=int(rating), comments=comments)
        return redirect('thank_you')
    return render(request, 'index.html')


def thank_you(request):
    return render(request, 'thank_you.html')
