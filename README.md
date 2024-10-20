# College Admission Management System - Backend

A Django REST API backend for managing Pakistani college admissions.

## Features

- User authentication with JWT
- Role-based access control
- Student profile management
- Program and course management
- Application tracking system
- Document upload and verification
- QR code generation for applications
- RESTful API with OpenAPI documentation

## Project Structure

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
└── templates/            # Django templates
```

## Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Update the following variables in `.env`:
- `SECRET_KEY`: Generate a new Django secret key
- `DATABASE_URL`: Configure your database connection
- `FRONT_END_URL`: Your frontend application URL
- Email settings for production

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Setup initial data
python manage.py setup_initial_data
```

### 4. Development Server

```bash
# Run development server
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

### 5. API Documentation

- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

## Docker Setup

### Development with Docker Compose

```bash
# Build and run services
docker-compose up --build

# Run migrations in container
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Setup initial data
docker-compose exec web python manage.py setup_initial_data
```

## Environment-Specific Settings

The project uses different settings for different environments:

- **Development**: `config.settings.development`
- **Production**: `config.settings.production`
- **Testing**: `config.settings.testing`

Set the `DJANGO_SETTINGS_MODULE` environment variable accordingly.

## Key Management Commands

```bash
# Setup initial data
python manage.py setup_initial_data

# Collect static files
python manage.py collectstatic

# Create migrations
python manage.py makemigrations

# Run tests
python manage.py test
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/refresh/` - Refresh token
- `POST /api/v1/auth/register/` - User registration

### Users
- `GET /api/v1/users/profile/` - Get user profile
- `PUT /api/v1/users/profile/` - Update user profile

### Programs
- `GET /api/v1/programs/` - List programs
- `POST /api/v1/programs/` - Create program

### Applications
- `GET /api/v1/applications/` - List applications
- `POST /api/v1/applications/` - Submit application
- `GET /api/v1/applications/{id}/` - Get application details

## Security Features

- JWT authentication
- CORS configuration
- SQL injection protection
- XSS protection
- CSRF protection
- Secure file uploads
- Rate limiting (recommended for production)

## Production Deployment

1. Set `DJANGO_SETTINGS_MODULE=config.settings.production`
2. Configure PostgreSQL database
3. Set up Redis for caching
4. Configure email backend
5. Set up static file serving (WhiteNoise or AWS S3)
6. Configure SSL/TLS
7. Set up monitoring and logging

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `python manage.py test`
4. Submit a pull request

## License

[Add your license information here]