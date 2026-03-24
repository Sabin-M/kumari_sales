from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # 🏠 Home
    path('', views.index, name='index'),

    # 🔐 Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),

    # 🏠 Categories
    path('home/', views.home_view, name='home'),
    path('fresh/', views.fresh, name='fresh'),
    path('sea/', views.sea, name='sea'),
    path('prawn/', views.prawn, name='prawn'),
    path('dry/', views.dry, name='dry'),

    # 📄 Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # 🔍 Search
    path('search/', views.search_products, name='search_products'),

    # 📦 Product
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    # 🛒 Cart
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('delete-cart/<int:id>/', views.delete_cart_item, name='delete_cart'),

    # 💳 Checkout (IMPORTANT FIX)
   path('checkout/', views.checkout, name='checkout'),
   path('checkout/<int:product_id>/', views.checkout, name='checkout'),

    # 📦 Orders
    path('order-success/<int:id>/', views.order_success, name='order_success'),
    path('track-order/<int:id>/', views.track_order, name='track_order'),
    path('order-pdf/<int:id>/', views.order_pdf, name='order_pdf'),
    path('my-orders/', views.my_orders, name='myorders'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)