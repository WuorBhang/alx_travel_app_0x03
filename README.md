# ALX Travel App - Milestone 5: Background Jobs with Celery

This project implements asynchronous background processing using Celery with RabbitMQ as the message broker. The main feature is an email notification system that sends booking confirmations without blocking the main request-response cycle.

## Features

- **Asynchronous Email Notifications**: Booking confirmations and payment confirmations are sent via email using Celery background tasks
- **Celery Integration**: Configured with RabbitMQ as the message broker
- **Django REST API**: RESTful API for listings, bookings, and payments
- **Payment Integration**: Chapa payment gateway integration
- **Swagger Documentation**: API documentation using drf-yasg

## Prerequisites

- Python 3.8+
- Django 5.2.5
- RabbitMQ (for message broker)
- SMTP email service (Gmail, SendGrid, etc.)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd alx_travel_app_0x03
   ```

2. **Install Python dependencies**
   ```bash
   cd alx_travel_app
   pip install -r requirements.txt
   ```

3. **Install and Start RabbitMQ**

   **On Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install rabbitmq-server
   sudo systemctl start rabbitmq-server
   sudo systemctl enable rabbitmq-server
   ```

   **On macOS:**
   ```bash
   brew install rabbitmq
   brew services start rabbitmq
   ```

   **On Windows:**
   Download and install from [RabbitMQ official website](https://www.rabbitmq.com/download.html)

4. **Configure Environment Variables**
   
   Create a `.env` file in the `alx_travel_app` directory:
   ```env
   CHAPA_SECRET_KEY=your_chapa_secret_key
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. **Update Email Settings**
   
   Edit `alx_travel_app/settings.py` and update the email configuration:
   ```python
   EMAIL_HOST_USER = 'your-email@gmail.com'  # Replace with your email
   EMAIL_HOST_PASSWORD = 'your-app-password'  # Replace with your app password
   DEFAULT_FROM_EMAIL = 'your-email@gmail.com'  # Replace with your email
   ```

6. **Run Database Migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

1. **Start Django Development Server**
   ```bash
   python manage.py runserver
   ```

2. **Start Celery Worker** (in a new terminal)
   ```bash
   cd alx_travel_app
   celery -A alx_travel_app worker --loglevel=info
   ```

3. **Start Celery Beat** (optional, for scheduled tasks)
   ```bash
   cd alx_travel_app
   celery -A alx_travel_app beat --loglevel=info
   ```

## Testing Celery Tasks

1. **Test Email Task Directly**
   ```bash
   python manage.py test_celery <booking_id>
   ```

2. **Test via API**
   - Create a booking via the API
   - Check the Celery worker logs for email task execution
   - Verify email delivery

## API Endpoints

- **Listings**: `GET/POST /api/listings/`
- **Bookings**: `GET/POST /api/bookings/`
- **Payments**: `POST /api/initiate-payment/`, `GET /api/verify-payment/<tx_ref>/`
- **API Documentation**: `/swagger/` or `/redoc/`

## Celery Configuration

The Celery configuration is located in `alx_travel_app/celery.py` and includes:

- **Message Broker**: RabbitMQ (`amqp://guest:guest@localhost:5672//`)
- **Result Backend**: RPC backend
- **Task Serialization**: JSON
- **Timezone**: UTC (configurable)

## Email Tasks

Two main Celery tasks are implemented:

1. **`send_booking_confirmation_email`**: Sends booking confirmation emails
2. **`send_payment_confirmation_email`**: Sends payment confirmation emails

These tasks are automatically triggered when:
- A new booking is created
- A payment is completed

## Project Structure

```
alx_travel_app/
├── alx_travel_app/
│   ├── __init__.py          # Celery app import
│   ├── celery.py            # Celery configuration
│   ├── settings.py          # Django settings with Celery config
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── listings/
│   ├── models.py            # Data models
│   ├── views.py             # API views with Celery task triggers
│   ├── tasks.py             # Celery shared tasks
│   ├── serializers.py       # DRF serializers
│   └── management/
│       └── commands/
│           └── test_celery.py  # Test command for Celery
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Troubleshooting

1. **RabbitMQ Connection Issues**
   - Ensure RabbitMQ service is running
   - Check if port 5672 is accessible
   - Verify RabbitMQ management plugin is enabled

2. **Email Delivery Issues**
   - Verify SMTP credentials in settings
   - Check email service provider settings
   - Ensure firewall allows SMTP connections

3. **Celery Worker Issues**
   - Check Celery worker logs for errors
   - Verify task imports in `__init__.py`
   - Ensure Django settings are properly configured

## Development

To add new Celery tasks:

1. Create the task function in `listings/tasks.py`
2. Decorate with `@shared_task`
3. Import and call the task from your views using `.delay()`

## Production Considerations

- Use environment variables for sensitive configuration
- Configure proper email backend (SendGrid, AWS SES, etc.)
- Set up monitoring for Celery workers
- Use Redis or PostgreSQL as result backend
- Configure proper logging and error handling

## License

This project is part of the ALX Software Engineering program.

## Contributing

This is an educational project. Please refer to the project requirements and guidelines.
