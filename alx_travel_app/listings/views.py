from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_booking_confirmation_email, send_payment_confirmation_email

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def perform_create(self, serializer):
        """
        Override perform_create to trigger email notification after booking creation.
        """
        # Save the booking first
        booking = serializer.save()
        
        # Trigger the email task asynchronously
        send_booking_confirmation_email.delay(booking.id)
        
        print(f"Booking created with ID: {booking.id}, email task triggered")


from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to the ALX Travel App Homepage!")


import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Payment

@api_view(['POST'])
def initiate_payment(request):
    booking_ref = request.data.get("booking_reference")
    amount = request.data.get("amount")
    email = request.data.get("email")

    payload = {
        "amount": amount,
        "currency": "ETB",
        "email": email,
        "tx_ref": booking_ref,
        "callback_url": "https://yourdomain.com/api/verify-payment/"
    }

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }

    response = requests.post("https://api.chapa.co/v1/transaction/initialize",
                              json=payload, headers=headers)

    data = response.json()

    if data.get("status") == "success":
        payment = Payment.objects.create(
            booking_reference=booking_ref,
            amount=amount,
            transaction_id=data["data"]["tx_ref"],
            status="Pending"
        )
        return Response(data)
    return Response(data, status=400)

@api_view(['GET'])
def verify_payment(request, tx_ref):
    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }

    url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
    response = requests.get(url, headers=headers)
    data = response.json()

    payment = get_object_or_404(Payment, transaction_id=tx_ref)

    if data.get("status") == "success" and data["data"]["status"] == "success":
        payment.status = "Completed"
        payment.save()
        # Trigger Celery email confirmation task
        send_payment_confirmation_email.delay(payment.id)
        print(f"Payment completed, email task triggered for payment ID: {payment.id}")
    else:
        payment.status = "Failed"
        payment.save()

    return Response(data)
