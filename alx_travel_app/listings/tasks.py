from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_booking_confirmation_email(booking_id):
    """
    Send a booking confirmation email to the user.
    This is a Celery shared task that runs in the background.
    """
    from .models import Booking
    
    try:
        # Get the booking object
        booking = Booking.objects.get(id=booking_id)
        
        # Prepare email content
        subject = f'Booking Confirmation - {booking.listing.title}'
        
        # Create HTML email content
        html_message = f"""
        <html>
        <body>
            <h2>Booking Confirmation</h2>
            <p>Dear {booking.user_name},</p>
            <p>Your booking has been confirmed successfully!</p>
            
            <h3>Booking Details:</h3>
            <ul>
                <li><strong>Property:</strong> {booking.listing.title}</li>
                <li><strong>Location:</strong> {booking.listing.location}</li>
                <li><strong>Check-in:</strong> {booking.check_in}</li>
                <li><strong>Check-out:</strong> {booking.check_out}</li>
                <li><strong>Price per night:</strong> ${booking.listing.price_per_night}</li>
                <li><strong>Booking ID:</strong> {booking.id}</li>
            </ul>
            
            <p>Thank you for choosing our travel platform!</p>
            <p>Best regards,<br>ALX Travel App Team</p>
        </body>
        </html>
        """
        
        # Create plain text version
        plain_message = strip_tags(html_message)
        
        # Send the email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.user_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"Booking confirmation email sent successfully to {booking.user_email}")
        return True
        
    except Booking.DoesNotExist:
        print(f"Booking with ID {booking_id} not found")
        return False
    except Exception as e:
        print(f"Error sending booking confirmation email: {str(e)}")
        return False


@shared_task
def send_payment_confirmation_email(payment_id):
    """
    Send a payment confirmation email to the user.
    This is a Celery shared task that runs in the background.
    """
    from .models import Payment
    
    try:
        # Get the payment object
        payment = Payment.objects.get(id=payment_id)
        
        # Prepare email content
        subject = f'Payment Confirmation - {payment.booking_reference}'
        
        # Create HTML email content
        html_message = f"""
        <html>
        <body>
            <h2>Payment Confirmation</h2>
            <p>Your payment has been processed successfully!</p>
            
            <h3>Payment Details:</h3>
            <ul>
                <li><strong>Booking Reference:</strong> {payment.booking_reference}</li>
                <li><strong>Transaction ID:</strong> {payment.transaction_id}</li>
                <li><strong>Amount:</strong> ${payment.amount}</li>
                <li><strong>Status:</strong> {payment.status}</li>
                <li><strong>Date:</strong> {payment.created_at}</li>
            </ul>
            
            <p>Thank you for your payment!</p>
            <p>Best regards,<br>ALX Travel App Team</p>
        </body>
        </html>
        """
        
        # Create plain text version
        plain_message = strip_tags(html_message)
        
        # For now, we'll use a default email since Payment model doesn't have user email
        # In a real application, you'd want to link Payment to User/Booking
        default_email = 'user@example.com'  # This should be replaced with actual user email
        
        # Send the email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[default_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"Payment confirmation email sent successfully")
        return True
        
    except Payment.DoesNotExist:
        print(f"Payment with ID {payment_id} not found")
        return False
    except Exception as e:
        print(f"Error sending payment confirmation email: {str(e)}")
        return False
