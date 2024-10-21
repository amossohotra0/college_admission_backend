# Pakistani College Admission Management System - API Documentation

## Overview
This is a comprehensive REST API for managing Pakistani college admissions with role-based access control, complete student profile management, application processing, and payment handling.

## Base URL
```
http://localhost:8000/api/v1/
```

## Authentication
The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## User Roles & Permissions

### 1. **Principal/Admin** (`admin`)
- Full system access
- Manage all users, programs, and settings
- View all reports and statistics

### 2. **Admission Officer** (`admission_officer`)
- Manage programs and academic sessions
- Review and approve/reject applications
- View admission statistics

### 3. **Application Reviewer** (`reviewer`)
- Review applications
- Update application status
- View application tracking

### 4. **Accountant** (`accountant`)
- Manage fee structures
- Verify payments
- Handle financial operations

### 5. **Data Entry Operator** (`data_entry`)
- Add/edit lookup data (degrees, institutes)
- Basic data management

### 6. **Student/Applicant** (`applicant`)
- Register and manage profile
- Submit applications
- Make payments
- Track application status

## API Endpoints

### Authentication Endpoints

#### Register New User
```http
POST /auth/register/
```
**Body:**
```json
{
    "email": "student@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "03001234567",
    "cnic": "12345-1234567-1",
    "password": "securepassword",
    "password2": "securepassword"
}
```

#### Login
```http
POST /auth/login/
```
**Body:**
```json
{
    "email": "student@example.com",
    "password": "securepassword"
}
```

#### Refresh Token
```http
POST /auth/refresh/
```
**Body:**
```json
{
    "refresh": "your_refresh_token"
}
```

#### Get/Update User Profile
```http
GET /auth/profile/
PUT /auth/profile/
```

### Student Profile Management

#### Student Profile
```http
GET /students/my_profile/          # Get own profile
POST /students/my_profile/         # Create profile
PUT /students/my_profile/          # Update profile
```

#### Personal Information
```http
GET /profile/personal-info/        # Get personal info
POST /profile/personal-info/       # Create personal info
PUT /profile/personal-info/        # Update personal info
```
**Body:**
```json
{
    "father_name": "Father Name",
    "cnic": "12345-1234567-1",
    "registered_contact": "03001234567",
    "date_of_birth": "2000-01-01",
    "gender": "male",
    "cnic_front_img": "file_upload",
    "cnic_back_img": "file_upload"
}
```

#### Contact Information
```http
GET /profile/contact-info/
POST /profile/contact-info/
PUT /profile/contact-info/
```
**Body:**
```json
{
    "district": "Lahore",
    "tehsil": "Model Town",
    "city": "Lahore",
    "permanent_address": "House 123, Street 1",
    "current_address": "House 123, Street 1",
    "postal_address": "House 123, Street 1"
}
```

#### Educational Background
```http
GET /educational-background/
POST /educational-background/
PUT /educational-background/{id}/
DELETE /educational-background/{id}/
```
**Body:**
```json
{
    "institution": 1,
    "degree": 1,
    "passing_year": 2020,
    "total_marks": 1100,
    "obtained_marks": 950,
    "grade": "A",
    "certificate": "file_upload"
}
```

#### Student Relatives
```http
GET /student-relatives/
POST /student-relatives/
PUT /student-relatives/{id}/
DELETE /student-relatives/{id}/
```

#### Medical Information
```http
GET /profile/medical-info/
POST /profile/medical-info/
PUT /profile/medical-info/
```

### Program Management

#### Programs
```http
GET /programs/                     # List all programs
POST /programs/                    # Create program (Admin/Admission Officer)
GET /programs/{id}/                # Get program details
PUT /programs/{id}/                # Update program
DELETE /programs/{id}/             # Delete program
```

#### Academic Sessions
```http
GET /academic-sessions/
POST /academic-sessions/           # Create session (Admin/Admission Officer)
GET /academic-sessions/{id}/
PUT /academic-sessions/{id}/
```

#### Offered Programs
```http
GET /offered-programs/             # List available programs for admission
POST /offered-programs/            # Create offering (Admin/Admission Officer)
GET /offered-programs/{id}/
```

### Application Management

#### Applications
```http
GET /applications/                 # List applications (filtered by role)
POST /applications/                # Submit application (Applicant only)
GET /applications/{id}/            # Get application details
```

**Submit Application Body:**
```json
{
    "program": 1,
    "academic_session": 1
}
```

#### Update Application Status
```http
POST /applications/{id}/update_status/    # (Reviewer/Admin/Admission Officer)
```
**Body:**
```json
{
    "status_id": 2,
    "remarks": "Application approved based on merit"
}
```

#### Application Tracking
```http
GET /applications/{id}/tracking/   # Get application status history
```

#### Application Statistics
```http
GET /applications/statistics/      # Get application statistics (Admin/Admission Officer)
```

### Payment Management

#### Payments
```http
GET /payments/                     # List payments (filtered by role)
POST /payments/                    # Create payment record (Applicant)
GET /payments/{id}/                # Get payment details
```

**Create Payment Body:**
```json
{
    "application": 1,
    "payment_type": "application",
    "amount": "1000.00",
    "payment_method": 1,
    "bank_reference": "TXN123456789",
    "receipt": "file_upload"
}
```

#### Verify Payment
```http
POST /payments/{id}/verify_payment/    # (Accountant/Admin)
```

#### Fee Structures
```http
GET /fee-structures/               # List fee structures
POST /fee-structures/              # Create fee structure (Admin/Admission Officer)
```

#### Payment Methods
```http
GET /payment-methods/              # List available payment methods
```

### Dashboard & Reports

#### Announcements
```http
GET /announcements/                # List announcements (role-filtered)
POST /announcements/               # Create announcement (Admin/Admission Officer)
GET /announcements/{id}/
PUT /announcements/{id}/
DELETE /announcements/{id}/
```

#### Admission Statistics
```http
GET /admission-stats/              # Get admission statistics (Admin/Admission Officer)
```

### Lookup Data

#### Degrees
```http
GET /degrees/                      # List all degrees
POST /degrees/                     # Add degree (Data Entry/Admin)
```

#### Institutes
```http
GET /institutes/                   # List all institutes
POST /institutes/                  # Add institute (Data Entry/Admin)
```

#### Blood Groups
```http
GET /blood-groups/                 # List blood groups
```

#### Diseases
```http
GET /diseases/                     # List diseases
```

#### Application Statuses
```http
GET /application-statuses/         # List application statuses (Reviewer+)
```

#### Roles
```http
GET /roles/                        # List all roles (Admin only)
```

## Sample Users for Testing

| Email | Password | Role | Description |
|-------|----------|------|-------------|
| admin@college.edu | admin123 | admin | Principal/Admin |
| admission@college.edu | admission123 | admission_officer | Admission Officer |
| accountant@college.edu | account123 | accountant | Accountant |
| reviewer@college.edu | review123 | reviewer | Application Reviewer |
| student@example.com | student123 | applicant | Test Student |

## Complete Admission Flow

### For Students:
1. **Register** → `POST /auth/register/`
2. **Login** → `POST /auth/login/`
3. **Complete Profile:**
   - Personal Info → `POST /profile/personal-info/`
   - Contact Info → `POST /profile/contact-info/`
   - Educational Background → `POST /educational-background/`
   - Medical Info → `POST /profile/medical-info/`
4. **Apply for Program** → `POST /applications/`
5. **Pay Application Fee** → `POST /payments/`
6. **Track Application** → `GET /applications/{id}/tracking/`

### For Admission Staff:
1. **Login** with staff credentials
2. **Review Applications** → `GET /applications/`
3. **Update Status** → `POST /applications/{id}/update_status/`
4. **Verify Payments** → `POST /payments/{id}/verify_payment/`
5. **Generate Reports** → `GET /applications/statistics/`

## Error Responses

All endpoints return appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

Error response format:
```json
{
    "error": "Error message",
    "details": "Detailed error information"
}
```

## API Documentation
- **Swagger UI**: http://localhost:8000/api/v1/docs/
- **ReDoc**: http://localhost:8000/api/v1/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/v1/schema/