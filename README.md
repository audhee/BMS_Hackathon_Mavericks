# Digital Border Management System - Backend

This is the Django-based backend for the Digital Border Management System. It integrates traveler identity verification with AI services and a MySQL database.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- MySQL Server

### 2. Setup Database
Create a MySQL database named `border_db`:
```sql
CREATE DATABASE border_db;
```

### 3. Install Dependencies
```bash
pip install django djangorestframework django-cors-headers mysqlclient requests
```

### 4. Configuration
Update `border_backend/settings.py` with your MySQL credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'border_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the Server
```bash
python manage.py runserver
```

## 🛠️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/verify-traveler/` | Verifies identity using OCR, Face Match, and Risk Assessment. |
| GET | `/api/traveler/{passport_number}/` | Retrieves traveler history and records. |
| POST | `/api/entry/` | Logs a new entry for an approved traveler. |

## 🧬 AI Core Services (Mocked in services.py)
- **OCR**: Extracts details from passport images.
- **Face Match**: Compares live image with passport biometric data.
- **Risk Assessment**: Calculates risk based on history, blacklist, and visa status.
