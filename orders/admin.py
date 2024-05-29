from django.contrib import admin
from .models import Order,OrderProduct

# Register your models here.
admin.site.register(OrderProduct)


class order(admin.ModelAdmin):
    list_display=['user','name','phone','email','address_line','state','city','order_total','status','is_ordered','created_at','updated_at','order_number','deliver_otp']

admin.site.register(Order,order)