
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
  
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('',views.home,name='home'),
    path('search',views.search,name='search') ,
    path('sellProducts/',views.sellProducts,name="sellProducts") ,
    path('confirm_order/', views.confirm_otp, name='confirm_order'),
    path('deliveryDetails/',views.deliveryDetails,name="deliveryDetails"),
    path('cold',views.cold,name="cold") ,
    path('cartnew/',views.cartnew,name='cartnew'),
    path('checkout/',views.checkout,name='checkout'),
    path('contact/',views.contact,name='contact'),
    path('dashboard/',views.farmer_requests,name='farmer_requests'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('<slug:slug>/<int:id>/',views.product,name='product'),
    path('<slug:slug>/',views.productView,name='productView') ,
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('confirm_order/<str:id>', views.confirm_otp, name='confirm_order'),

]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
