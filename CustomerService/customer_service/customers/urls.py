from django.urls import path
from .views import CustomerView, CustomerAddressView, CustomerWithAddressView

urlpatterns = [
    path('customers/', CustomerView.as_view(), name="customers"),
    path('customers/<int:customer_id>/', CustomerView.as_view(), name="customer-detail"),
    path('customer-addresses/', CustomerAddressView.as_view(), name="customer-addresses"),
    path('customer-addresses/<int:address_id>/', CustomerAddressView.as_view(), name="customer-address-detail"),
    path('customers-with-address/', CustomerWithAddressView.as_view(), name='create_customer_with_address'),
]
