from .models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        count = sum(item.quantity for item in cart_items)
    else:
        count = 0

    return {'cart_count': count}