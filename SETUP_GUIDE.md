# College Admission Management System - Setup Guide

## Prerequisites

- Python 3.8+ installed
- Git installed
- Basic knowledge of Django and REST APIs

## Quick Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd backend
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
cp .env.example .env
```

Edit `.env` file and update:
```env
SECRET_KEY=your-generated-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py setup_initial_data
```

### 6. Run Server
```bash
python manage.py runserver
```

Visit: http://localhost:8000/api/v1/docs/

## Detailed Setup Instructions

### Environment Variables (.env)

Create `.env` file with these settings:

```env
# Core Settings
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
DJANGO_SETTINGS_MODULE=config.settings.development

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Static/Media Files
STATIC_URL=/static/
STATIC_ROOT=staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=media

# CORS
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Frontend URLs
FRONT_END_URL=http://localhost:3000
VERIFICATION_URL=http://localhost:3000/verify/

# Security
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=30
JWT_REFRESH_TOKEN_LIFETIME=1440
```

### Database Options

#### SQLite (Default - Development)
```env
DATABASE_URL=sqlite:///db.sqlite3
```

#### PostgreSQL (Production)
```bash
pip install psycopg2-binary
```
```env
DATABASE_URL=postgresql://username:password@localhost:5432/college_admission_db
```

### Initial Data Population

The `setup_initial_data` command creates:

**User Roles:**
- Principal/Admin
- Admission Officer  
- Application Reviewer
- Accountant
- Data Entry Operator
- Student/Applicant

**Application Statuses:**
- Submitted
- Under Review
- Approved
- Rejected
- Waitlisted

**Sample Programs:**
- Bachelor of Science in Computer Science
- Bachelor of Science in Electrical Engineering
- Bachelor of Science in Mechanical Engineering
- Bachelor of Business Administration

**Test Users:**
| Email | Password | Role |
|-------|----------|------|
| admin@college.edu | admin123 | admin |
| admission@college.edu | admission123 | admission_officer |
| accountant@college.edu | account123 | accountant |
| reviewer@college.edu | review123 | reviewer |
| student@example.com | student123 | applicant |

**Lookup Data:**
- Degrees (Matric, Intermediate, Bachelor, Master, PhD)
- Institutes (Sample Pakistani institutions)
- Blood Groups (A+, A-, B+, B-, AB+, AB-, O+, O-)
- Payment Methods (Bank Transfer, JazzCash, EasyPaisa, etc.)

## Docker Setup (Optional)

### Development with Docker
```bash
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py setup_initial_data
```

### Production Docker
```bash
docker build -t college-admission .
docker run -p 8000:8000 college-admission
```

## Testing the Setup

### 1. Check API Documentation
Visit: http://localhost:8000/api/v1/docs/

### 2. Test Authentication
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "student@example.com", "password": "student123"}'
```

### 3. Test Protected Endpoint
```bash
curl -X GET http://localhost:8000/api/v1/programs/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Development Workflow

### 1. Create New App
```bash
python manage.py startapp new_app_name apps/new_app_name
```

### 2. Add to INSTALLED_APPS
```python
# config/settings/base.py
LOCAL_APPS = [
    'apps.users',
    'apps.programs',
    'apps.applications',
    'apps.payments',
    'apps.dashboard',
    'apps.api',
    'apps.common',
    'apps.new_app_name',  # Add here
]
```

### 3. Create Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run Tests
```bash
python manage.py test
```

## Production Deployment

### 1. Environment Setup
```env
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
DATABASE_URL=postgresql://user:pass@host:5432/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 2. Static Files
```bash
python manage.py collectstatic --noinput
```

### 3. Security Settings
```env
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Troubleshooting

### Common Issues

#### 1. Migration Errors
```bash
python manage.py makemigrations --empty app_name
python manage.py migrate --fake-initial
```

#### 2. Permission Denied
```bash
chmod +x manage.py
```

#### 3. Port Already in Use
```bash
python manage.py runserver 8001
```

#### 4. Database Connection Error
Check DATABASE_URL in .env file and ensure database exists.

### Reset Database
```bash
rm db.sqlite3
python manage.py migrate
python manage.py setup_initial_data
```

## API Testing Tools

### Using curl
```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "student@example.com", "password": "student123"}' \
  | jq -r '.access')

# Use token
curl -X GET http://localhost:8000/api/v1/programs/ \
  -H "Authorization: Bearer $TOKEN"
```

### Using Postman
1. Import API collection from Swagger
2. Set up environment variables
3. Use Bearer token authentication

## File Structure
```
backend/
├── apps/                   # Django applications
│   ├── api/               # API endpoints
│   ├── applications/      # Application management
│   ├── common/           # Shared utilities
│   ├── dashboard/        # Dashboard functionality
│   ├── payments/         # Payment processing
│   ├── programs/         # Academic programs
│   └── users/            # User management
├── config/               # Django configuration
│   └── settings/         # Environment-specific settings
├── logs/                 # Application logs
├── media/                # User uploaded files
├── staticfiles/          # Static files
├── templates/            # Django templates
├── venv/                 # Virtual environment
├── .env                  # Environment variables
├── .gitignore           # Git ignore rules
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Support

For issues or questions:
1. Check the API documentation at `/api/v1/docs/`
2. Review the error logs in `logs/django.log`
3. Ensure all environment variables are set correctly
4. Verify database migrations are applied