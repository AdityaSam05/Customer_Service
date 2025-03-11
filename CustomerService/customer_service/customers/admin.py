from django.contrib import admin
from .models import Customer, CustomerAddress

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'first_name', 'last_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('created_at',)

@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'customer', 'street_address', 'city', 'state', 'pincode', 'country', 'created_at')
    search_fields = ('street_address', 'city', 'state', 'pincode', 'customer__first_name', 'customer__last_name')
    list_filter = ('city', 'state', 'country', 'created_at')
