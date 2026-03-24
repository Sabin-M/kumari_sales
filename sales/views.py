from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, LoginForm
from .models import Product, Order, OrderItem, Cart

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from django.contrib.auth.decorators import login_required
from django.db import transaction
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.utils.text import slugify
from django.urls import reverse

# 🏠 Landing Page
def index(request):
    return render(request, 'index.html')


# 📝 Signup (FIXED)
def signup_view(request):
    error = None

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=email).exists():
                error = "Email already registered"
            else:
                User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )
                return redirect('login')
    else:
        form = PostForm()

    return render(request, 'signup.html', {'form': form, 'error': error})


# 🔐 Login (FIXED)
def login_view(request):
    error = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
            else:
                error = "Invalid email or password"
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'error': error})


# 🚪 Logout
def logout_view(request):
    logout(request)
    return redirect('login')


# 🏠 Category Views
def home_view(request):
    products = Product.objects.filter(category='home')
    return render(request, 'home.html', {'products': products})


def fresh(request):
    return render(request, 'fresh.html', {
        'products': Product.objects.filter(category='fresh')
    })


def sea(request):
    return render(request, 'sea.html', {
        'products': Product.objects.filter(category='sea')
    })


def prawn(request):
    return render(request, 'prawn.html', {
        'products': Product.objects.filter(category='prawn')
    })


def dry(request):
    return render(request, 'dry.html', {
        'products': Product.objects.filter(category='dry')
    })


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# 🔍 Search
def search_products(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        products = Product.objects.filter(name__icontains=query)[:10]

        for item in products:
            results.append({
                "id": item.id,
                "name": item.name,
                "price": str(item.price),
                "image": item.image.url if item.image else "",
                "slug": slugify(item.name),
                "page": item.category,
                "url": reverse('product_detail', args=[item.id])   # ✅ NEW
            })

    return JsonResponse(results, safe=False)


# 📦 Product Detail
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


# 🛒 Add to Cart (FIXED)
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.GET.get('quantity', 1))

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    new_quantity = cart_item.quantity + quantity if not created else quantity

    if new_quantity > product.stock:
        return redirect('cart')

    cart_item.quantity = new_quantity
    cart_item.save()

    return redirect('cart')


# 🛒 Cart Page (FIXED)
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# ❌ Delete Cart Item
@login_required
def delete_cart_item(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    item.delete()
    return redirect('cart')


@login_required
def checkout(request, product_id=None):

    buy_now = False
    product = None
    cart_items = []
    total = 0
    quantity = 1

    # ================= BUY NOW =================
    if product_id:
        buy_now = True
        product = get_object_or_404(Product, id=product_id)

        if request.method == "POST":
            quantity = int(request.POST.get('quantity', 1))

        total = product.price * quantity

    # ================= CART =================
    else:
        cart_items = Cart.objects.filter(user=request.user)

        for item in cart_items:
            total += item.product.price * item.quantity

    # ================= PLACE ORDER =================
    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        country = request.POST.get('country')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        alt_mobile = request.POST.get('alt_mobile')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        payment = request.POST.get('payment')

        # 🛑 validation
        if not first_name or not address:
            return render(request, 'checkout.html', {
                'error': 'Please fill required fields',
                'product': product,
                'quantity': quantity,
                'cart_items': cart_items,
                'buy_now': buy_now,
                'total': total
            })

        # ✅ FIXED HERE (total_amount)
        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            country=country,
            address=address,
            mobile=mobile,
            alt_mobile=alt_mobile,
            city=city,
            state=state,
            pincode=pincode,
            payment_method=payment,
            total_amount=total   # ✅ FIXED
        )

        # ================= ORDER ITEMS =================

        # 🟩 BUY NOW
        if buy_now:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        # 🟦 CART
        else:
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            cart_items.delete()

        # ✅ VERY IMPORTANT FIX
        return redirect('order_success', order.id)

    # ================= PAGE LOAD =================
    return render(request, 'checkout.html', {
        'product': product,
        'quantity': quantity,
        'cart_items': cart_items,
        'buy_now': buy_now,
        'total': total
    })

# ✅ Order Success
@login_required
def order_success(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    order_items = order.items.all()

    return render(request, 'order_success.html', {
        'order': order,
        'order_items': order_items
    })


# 📦 My Orders
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'my_orders.html', {
        'orders': orders
    })
    
def track_order(request, id):
    order = Order.objects.get(id=id)
    return render(request, 'track_order.html', {'order': order})

@login_required
def order_pdf(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    order_items = order.items.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Order_{order.id}.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    elements = []

    # ================= TITLE =================
    elements.append(Paragraph(f"Order Invoice - #{order.id}", styles['Title']))
    elements.append(Spacer(1, 10))

    # ================= CUSTOMER DETAILS =================
    elements.append(Paragraph("Customer Details", styles['Heading2']))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(f"Name: {order.first_name} {order.last_name}", styles['Normal']))
    elements.append(Paragraph(f"Mobile: {order.mobile}", styles['Normal']))
    elements.append(Paragraph(f"Address: {order.address}", styles['Normal']))
    elements.append(Paragraph(f"City: {order.city}", styles['Normal']))
    elements.append(Paragraph(f"State: {order.state}", styles['Normal']))
    elements.append(Paragraph(f"Pincode: {order.pincode}", styles['Normal']))
    elements.append(Paragraph(f"Country: {order.country}", styles['Normal']))

    elements.append(Spacer(1, 15))

    # ================= ORDER DETAILS =================
    elements.append(Paragraph("Order Details", styles['Heading2']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"Payment Method: {order.payment_method}", styles['Normal']))
    elements.append(Paragraph(f"Status: {order.status}", styles['Normal']))

    elements.append(Spacer(1, 15))

    # ================= TABLE =================
    data = [['Product', 'Price', 'Quantity', 'Total']]

    for item in order_items:
        data.append([
            item.product.name,
            f"₹{item.price}",
            item.quantity,
            f"₹{item.price * item.quantity}"
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ]))

    elements.append(table)

    elements.append(Spacer(1, 20))

    # ================= TOTAL =================
    elements.append(Paragraph(f"Grand Total: ₹{order.total_amount}", styles['Heading2']))

    doc.build(elements)

    return response