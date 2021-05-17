from django.contrib import admin
from .models import Customer,Cart,Order_placed,Product
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','name','locality','city','pin','state']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','price','description','discount_price','brand','category','product_image']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(Order_placed)
class Order_placedAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer_info', 'product_info', 'order_date','quantity','status']

# Show Product and Customer info in Order Placed Admin Page
    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)

    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)