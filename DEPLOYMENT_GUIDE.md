# ALX Travel App - Deployment Guide

This guide provides step-by-step instructions for deploying the ALX Travel App to production with Celery background tasks and public Swagger documentation.

## 🚀 Deployment Options

### Option 1: Render (Recommended)

Render provides excellent support for Django applications with PostgreSQL and Redis.

#### Prerequisites
- GitHub account with your code repository
- Render account (free tier available)

#### Steps

1. **Prepare Your Repository**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Create Render Services**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Configure Environment Variables**
   Set these environment variables in Render:
   ```
   SECRET_KEY=your-production-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=*.render.com
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   CHAPA_SECRET_KEY=your_chapa_secret_key_here
   ```

4. **Deploy**
   - Render will automatically deploy your app
   - The web service will be available at `https://your-app-name.onrender.com`
   - Swagger documentation will be at `https://your-app-name.onrender.com/swagger/`

### Option 2: Heroku

#### Prerequisites
- Heroku CLI installed
- Heroku account

#### Steps

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Add Add-ons**
   ```bash
   heroku addons:create heroku-postgresql:mini
   heroku addons:create heroku-redis:mini
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-production-secret-key-here
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   heroku config:set EMAIL_HOST_USER=your-email@gmail.com
   heroku config:set EMAIL_HOST_PASSWORD=your-app-password
   heroku config:set CHAPA_SECRET_KEY=your_chapa_secret_key_here
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Scale Celery Worker**
   ```bash
   heroku ps:scale worker=1
   ```

### Option 3: PythonAnywhere

#### Prerequisites
- PythonAnywhere account

#### Steps

1. **Upload Code**
   - Upload your code to PythonAnywhere via Git or file upload

2. **Create Web App**
   - Go to Web tab → Add a new web app
   - Choose Django
   - Set source code path to your project directory

3. **Configure WSGI**
   - Edit the WSGI configuration file
   - Point it to your `alx_travel_app.wsgi` module

4. **Set Environment Variables**
   - Add environment variables in the Web tab

5. **Configure Static Files**
   - Set static files mapping: `/static/` → `/path/to/your/staticfiles/`

6. **Setup Celery (Manual)**
   - PythonAnywhere doesn't support background tasks on free tier
   - Consider upgrading to a paid plan for Celery support

## 🔧 Configuration Details

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `your-secret-key-here` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `your-domain.com,*.render.com` |
| `DATABASE_URL` | Database connection | `postgresql://user:pass@host:port/db` |
| `CELERY_BROKER_URL` | Celery broker | `redis://localhost:6379/0` |
| `CELERY_RESULT_BACKEND` | Celery results | `redis://localhost:6379/0` |
| `EMAIL_HOST_USER` | Email username | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Email password | `your-app-password` |
| `CHAPA_SECRET_KEY` | Payment gateway key | `your-chapa-key` |

### Database Migration

After deployment, run migrations:
```bash
python manage.py migrate
```

### Static Files

Collect static files:
```bash
python manage.py collectstatic --noinput
```

### Create Superuser

Create an admin user:
```bash
python manage.py createsuperuser
```

## 📊 Testing Deployment

### 1. Test Web Application
- Visit your deployed URL
- Check that the homepage loads
- Verify admin panel access at `/admin/`

### 2. Test API Endpoints
- Visit `/swagger/` for API documentation
- Test the following endpoints:
  - `GET /api/listings/` - List all listings
  - `POST /api/bookings/` - Create a booking
  - `POST /initiate-payment/` - Initiate payment

### 3. Test Celery Tasks
- Create a booking via API
- Check email delivery
- Monitor Celery worker logs

### 4. Test Swagger Documentation
- Visit `https://your-domain.com/swagger/`
- Verify all endpoints are documented
- Test API calls directly from Swagger UI

## 🔍 Monitoring and Debugging

### Check Logs
```bash
# Render
Check logs in Render dashboard

# Heroku
heroku logs --tail

# PythonAnywhere
Check error logs in Files tab
```

### Common Issues

1. **Static Files Not Loading**
   - Ensure `STATIC_ROOT` is set correctly
   - Run `collectstatic` command
   - Check WhiteNoise configuration

2. **Database Connection Issues**
   - Verify `DATABASE_URL` is set correctly
   - Check database credentials
   - Ensure migrations are run

3. **Celery Tasks Not Running**
   - Check Celery worker is running
   - Verify broker connection (Redis/RabbitMQ)
   - Check task logs for errors

4. **Email Not Sending**
   - Verify email credentials
   - Check SMTP settings
   - Test email configuration

## 🔒 Security Checklist

- [ ] `DEBUG = False` in production
- [ ] Strong `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] Database credentials secured
- [ ] Email credentials secured
- [ ] HTTPS enabled
- [ ] Static files served securely

## 📈 Performance Optimization

1. **Database Optimization**
   - Use connection pooling
   - Optimize database queries
   - Add database indexes

2. **Caching**
   - Implement Redis caching
   - Cache API responses
   - Use template caching

3. **Static Files**
   - Use CDN for static files
   - Enable compression
   - Set proper cache headers

## 🎯 Post-Deployment Tasks

1. **Monitor Application**
   - Set up error tracking (Sentry)
   - Monitor performance metrics
   - Set up uptime monitoring

2. **Backup Strategy**
   - Regular database backups
   - Code repository backups
   - Environment configuration backups

3. **Scaling**
   - Monitor resource usage
   - Scale web dynos/workers as needed
   - Optimize database performance

## 📞 Support

If you encounter issues during deployment:

1. Check the logs for error messages
2. Verify all environment variables are set
3. Ensure all dependencies are installed
4. Test locally before deploying
5. Consult platform-specific documentation

## 🎉 Success!

Once deployed successfully, your ALX Travel App will be available with:
- ✅ Public API endpoints
- ✅ Swagger documentation at `/swagger/`
- ✅ Background email notifications via Celery
- ✅ Payment processing integration
- ✅ Admin interface at `/admin/`

Your application is now ready for production use!