# ABCPET - Pet Care Services Platform

![ABCPET](https://abcpet.co/static/img/logo.png)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Contact](#contact)

## Overview

ABCPET is a comprehensive platform connecting pet owners with pet care service providers. The application allows users to register their pets, find verified pet sitters, walkers, and boarding services in their area, and manage bookings and payments through a secure system.

**Website:** [https://abcpet.co](https://abcpet.co)

## Features

### User Authentication & Management
- Multi-step registration process with email verification
- OTP-based authentication
- User profile management
- Login history tracking for security

### Pet Management
- Pet profile creation and management
- Support for multiple pets per user
- Detailed pet information including health records, medication details, and care instructions

### Service Provider Features
- Host registration and verification system
- Service offering configuration (boarding, pet sitting, walking, day care)
- Availability calendar management
- Rate setting
- Service area definition
- Photo gallery for accommodation

### Search & Discovery
- Location-based service provider search
- Filtering by service type, availability, and price
- Host profiles with ratings and reviews

### Booking System
- In-app booking requests
- Booking management dashboard
- Calendar integration

### Payment Processing
- Secure payment methods
- Wallet system for users
- Transaction history

### Admin Dashboard
- User management
- Host verification controls
- Site settings configuration
- Reporting and analytics

## Technologies Used

### Backend
- **Python 3.x**
- **Django 5.2**: Web framework
- **Django REST Framework 3.16**: API development
- **SQLite** (Development) / Production Database (Configurable)

### Frontend
- **HTML/CSS/JavaScript**
- **Bootstrap**: UI framework
- **jQuery**: JavaScript library

### Deployment & Infrastructure
- **WhiteNoise 6.9.0**: Static file serving
- **Azure Web App**: Hosting platform

### Security
- Token-based authentication
- CSRF protection
- Session security

## Architecture

The application follows a Django MVT (Model-View-Template) architecture:

### Project Structure
```
abcpet/
├── abcpet_project/             # Main project settings
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL routing
│   ├── wsgi.py                 # WSGI application
│   ├── asgi.py                 # ASGI configuration
│   └── __init__.py             # Python package identifier
├── abcpet_app/                 # Main application module
│   ├── admin.py                # Admin panel configuration
│   ├── apps.py                 # App configuration
│   ├── authentication_backends.py # Custom auth backends
│   ├── constants.py            # Application constants
│   ├── context_processors.py   # Template context processors
│   ├── forms.py                # Form definitions
│   ├── host_image.py           # Host image processing
│   ├── middleware/             # Custom middleware
│   │   ├── __init__.py
│   │   ├── login_middleware.py  # Login tracking
│   │   └── admin_middleware.py  # Admin access control
│   ├── migrations/             # Database migrations
│   │   └── __init__.py
│   ├── models.py               # Data models
│   ├── serializers.py          # REST API serializers
│   ├── static/                 # App-specific static files
│   │   ├── css/                # Stylesheets
│   │   │   ├── dashboard.css
│   │   │   ├── login.css
│   │   │   └── main.css
│   │   ├── js/                 # JavaScript files
│   │   │   ├── dashboard.js
│   │   │   ├── host-registration.js
│   │   │   ├── pet-management.js
│   │   │   └── validation.js
│   │   └── img/                # Images
│   │       ├── icons/
│   │       └── backgrounds/
│   ├── templates/              # HTML templates
│   │   ├── abcpet_app/         # App-specific templates
│   │   │   ├── admin/          # Admin templates
│   │   │   │   ├── dashboard.html
│   │   │   │   ├── host_verification.html
│   │   │   │   └── user_management.html
│   │   │   ├── auth/           # Authentication templates
│   │   │   │   ├── login.html
│   │   │   │   ├── signup.html
│   │   │   │   ├── email_confirmation.html
│   │   │   │   └── password_reset.html
│   │   │   ├── dashboard/      # User dashboard templates
│   │   │   │   ├── index.html
│   │   │   │   ├── profile.html
│   │   │   │   └── settings.html
│   │   │   ├── hosts/          # Host-related templates
│   │   │   │   ├── registration.html
│   │   │   │   ├── profile.html
│   │   │   │   └── search.html
│   │   │   ├── pets/           # Pet management templates
│   │   │   │   ├── create.html
│   │   │   │   ├── edit.html
│   │   │   │   └── detail.html
│   │   │   └── base.html       # Base template with common elements
│   │   └── emails/             # Email templates
│   │       ├── confirmation.html
│   │       ├── reset_password.html
│   │       └── welcome.html
│   ├── tests/                  # Test cases
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── test_forms.py
│   ├── urls.py                 # App URL routing
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── email_utils.py      # Email sending utilities
│   │   └── validators.py       # Custom validators
│   └── views.py                # View controllers
├── static/                     # Project-wide static files
│   ├── admin/                  # Admin static files
│   ├── css/                    # Global CSS
│   │   ├── bootstrap/          # Bootstrap framework
│   │   └── custom/             # Custom styles
│   ├── js/                     # Global JavaScript
│   │   ├── jquery/            # jQuery library
│   │   └── custom/            # Custom scripts
│   ├── img/                    # Global images
│   └── fonts/                  # Web fonts
├── media/                      # User uploaded content
│   ├── profile_pictures/       # User profile images
│   ├── mascota_photos/         # Pet photos
│   ├── fotos_casa/             # Host home photos
│   ├── fotos_perfil/           # Host profile photos
│   ├── fotos_id/               # Host ID verification
│   └── fotos_domicilio/        # Host address verification
├── templates/                  # Project-wide templates
│   ├── 404.html                # Error pages
│   ├── 500.html
│   └── base.html               # Site-wide base template
├── manage.py                   # Django management script
├── requirements.txt            # Project dependencies
├── Procfile                    # Deployment configuration
└── README.md                   # Project documentation
```

### Key Models

1. **CustomUser**: Extended Django user model with email confirmation
2. **UserProfile**: User details including address and preferences
3. **Mascota**: Pet information and care details
4. **ABCPetHost**: Service provider profiles and offering details
5. **UserWallet**: In-app financial tracking
6. **LoginDetail**: Security tracking of login attempts

### Authentication Flow
The application implements a multi-step authentication process:
1. Email registration
2. Email verification via token
3. OTP verification
4. Profile completion
5. Login with username/email and password

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/peterfulle/abcpet.git
   cd abcpet
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   ```

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000`

## Usage

### Admin Access
1. Navigate to `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials

### User Registration
1. Navigate to the signup page
2. Complete the multi-step registration process
3. Verify your email address

### Pet Registration
1. Login to your account
2. Navigate to the dashboard
3. Click "Add Pet"
4. Complete the pet profile form

### Service Provider Registration
1. Login to your account
2. Navigate to "Become a Host"
3. Complete the host registration process
4. Wait for admin approval

### Searching for Services
1. Browse available hosts by location
2. Filter by service type and price
3. View host profiles and reviews
4. Send booking requests

## API Documentation

The application provides a REST API for integration with mobile applications or third-party services:

### Authentication Endpoints
- **POST** `/api/token/`: Obtain authentication token
- **POST** `/api/token/refresh/`: Refresh authentication token

### User Endpoints
- **GET** `/api/userprofile/`: Get user profile information
- **PUT** `/api/userprofile/`: Update user profile

### Additional endpoints available through Django REST Framework browsable API

## Deployment

### Azure Web App Deployment

The application is configured for deployment to Azure Web App:

1. Create an Azure Web App resource
2. Configure the deployment settings using GitHub Actions or Azure DevOps
3. Add the necessary environment variables in Azure App Configuration
4. Deploy the application

### Configuration

The application includes a `Procfile` for cloud deployment platforms:
```
web: python manage.py runserver
```

For production, update `settings.py` with appropriate production settings:
- Set `DEBUG = False`
- Configure a production-ready database
- Set proper ALLOWED_HOSTS

## Contributing

We welcome contributions to improve ABCPET:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contact

**Developer:** Peter Fulle - [peterfulle](https://github.com/peterfulle)

**Project Repository:** [https://github.com/peterfulle/abcpet](https://github.com/peterfulle/abcpet)

**Last Updated:** 2025-05-08