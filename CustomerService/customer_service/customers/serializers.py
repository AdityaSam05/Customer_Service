from rest_framework import serializers
from .models import Customer, CustomerAddress

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = '__all__'
        read_only_fields = ['customer']

class CustomerSerializer(serializers.ModelSerializer):
    addresses = CustomerAddressSerializer(many=True, required=False)

    class Meta:
        model = Customer
        fields = ['customer_id', 'first_name', 'last_name', 'email', 'phone', 'created_at', 'addresses']

class CustomerCreateSerializer(serializers.ModelSerializer):
    addresses = CustomerAddressSerializer(many=True)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'addresses']

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        customer = Customer.objects.create(**validated_data)
        for address_data in addresses_data:
            CustomerAddress.objects.create(customer=customer, **address_data)
        return customer
