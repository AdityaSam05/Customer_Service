from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from django.db import transaction
from .serializers import CustomerSerializer, CustomerAddressSerializer, CustomerCreateSerializer
from .models import Customer, CustomerAddress
from .exceptions import (
    CustomerNotFoundException, 
    InvalidDataException, 
    InternalServerException, 
    NotFoundException,
    BadRequestException,
    ConflictException,
    ThrottledException,
    PermissionDeniedException,
)

class CustomThrottle(UserRateThrottle):
    rate = "10000/min"  # Allow 10000 requests per minute per user

    def allow_request(self, request, view):
        if request.method != "GET":  # Apply throttling only to GET requests
            return True  
        if not super().allow_request(request, view):
            raise ThrottledException()
        return True

class CustomerView(APIView):
    """Handles Customer CRUD operations"""
    throttle_classes = [CustomThrottle]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, customer_id=None):
        if customer_id:
            try:
                customer = Customer.objects.get(pk=customer_id)
            except Customer.DoesNotExist:
                raise CustomerNotFoundException()
            
            addresses = CustomerAddress.objects.filter(customer=customer)
            data = {
                "customer_id": customer.customer_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "phone": customer.phone,
                "created_at": customer.created_at,
                "addresses": CustomerAddressSerializer(addresses, many=True).data,
            }
            return Response(data, status=status.HTTP_200_OK)
        
        customers = Customer.objects.all()
        data = CustomerSerializer(customers, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.data:
            raise BadRequestException("Request body cannot be empty.")
        
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                customer = serializer.save()
                return Response(CustomerSerializer(customer).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise ConflictException(str(e))
        raise InvalidDataException(serializer.errors)

    def put(self, request, customer_id):
        """Update customer details"""
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise CustomerNotFoundException()

        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise InvalidDataException(serializer.errors)

    def patch(self, request, customer_id):
        """Partially update customer details"""
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise CustomerNotFoundException()

        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise InvalidDataException(serializer.errors)

    def delete(self, request, customer_id):
        """Delete a customer"""
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise CustomerNotFoundException()
        
        customer.delete()
        return Response({"message": "Customer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class CustomerAddressView(APIView):
    """Handles Address CRUD operations"""
    throttle_classes = [CustomThrottle]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        addresses = CustomerAddress.objects.select_related('customer').all()
        serializer = CustomerAddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.data:
            raise BadRequestException("Request body cannot be empty.")
        
        customer_id = request.data.get('customer_id')
        if not customer_id:
            raise InvalidDataException({"customer_id": "Customer ID is required."})
        
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise CustomerNotFoundException()
        
        serializer = CustomerAddressSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(customer=customer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise ConflictException(str(e))
        raise InvalidDataException(serializer.errors)
    
    def put(self, request, address_id):
        """Update an address"""
        try:
            address = CustomerAddress.objects.get(pk=address_id)
        except CustomerAddress.DoesNotExist:
            raise NotFoundException()

        serializer = CustomerAddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise InvalidDataException(serializer.errors)

    def patch(self, request, address_id):
        """Partially update an address"""
        try:
            address = CustomerAddress.objects.get(pk=address_id)
        except CustomerAddress.DoesNotExist:
            raise NotFoundException()

        serializer = CustomerAddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise InvalidDataException(serializer.errors)

    def delete(self, request, address_id):
        """Delete an address"""
        try:
            address = CustomerAddress.objects.get(pk=address_id)
        except CustomerAddress.DoesNotExist:
            raise NotFoundException()
        
        address.delete()
        return Response({"message": "Address deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class CustomerWithAddressView(APIView):
    """Handles Customer creation along with address"""
    throttle_classes = [CustomThrottle]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def post(self, request):
        if not request.data:
            raise BadRequestException("Request body cannot be empty.")
        
        serializer = CustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    customer = serializer.save()
                    response_serializer = CustomerSerializer(customer)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise InternalServerException(detail=str(e))
        raise InvalidDataException(serializer.errors)