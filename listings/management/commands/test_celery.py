from django.core.management.base import BaseCommand
from listings.tasks import send_booking_confirmation_email


class Command(BaseCommand):
    help = 'Test Celery task execution'

    def add_arguments(self, parser):
        parser.add_argument('booking_id', type=int, help='ID of the booking to test email')

    def handle(self, *args, **options):
        booking_id = options['booking_id']
        
        self.stdout.write(
            self.style.SUCCESS(f'Testing Celery task for booking ID: {booking_id}')
        )
        
        try:
            # Execute the task synchronously for testing
            result = send_booking_confirmation_email(booking_id)
            
            if result:
                self.stdout.write(
                    self.style.SUCCESS('Email task executed successfully!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('Email task failed!')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error executing task: {str(e)}')
            )
