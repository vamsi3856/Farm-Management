from django.contrib import admin
from .models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=('category_name','slug')

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'product_slug':('product_name',)}
    list_display=('product_name','product_slug')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Payment)
admin.site.register(ReviewRating)
admin.site.register(Contact)





