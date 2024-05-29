from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns=[
    path('payments/',views.payments,name='payments'),
    path('place_order/',views.place_order,name='place_order'),
    path('invoice/<int:id>/', views.invoice, name='invoice'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('order_history/', views.order_history, name='order_history'),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)