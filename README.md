# Health_Insurance

Health_Insurance is a Django-based web application for managing and purchasing health insurance plans.  
It allows users to explore insurance plans, add them to cart, make payments, and manage policies, while admins can manage plans, users.

This project is built using Django with a template-based frontend (HTML, CSS, Bootstrap).

---

## 🚀 Features

### 👤 Customer Features
- User Registration & Login
- Browse and search health insurance plans
- View plan details
- Add plans to cart
- Secure payment integration (PayPal Sandbox)
- Policy purchase and invoice generation
- View active and expired policies
- Profile management with profile picture upload

### 🛠 Admin Features
- Admin Dashboard
- Manage insurance plans (Create, Read, Update, Delete)
- View and manage customer profiles
- Admin profile management

---

## 🧑‍💻 Tech Stack

- Backend: Django (Python)
- Frontend: HTML, CSS, Bootstrap
- Database: SQLite (default)
- Payment Gateway: PayPal (Sandbox Integration)
- Authentication: Django Built-in Authentication System

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/...
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Virtual Environment

#### Windows:
```bash
venv\Scripts\activate
```

#### Mac/Linux:
```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Apply Migrations

```bash
python manage.py migrate
```

### 6️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

### 7️⃣ Run Development Server

```bash
python manage.py runserver
```

#### Project will run at:
```cpp
http://127.0.0.1:8000/
```
#### settings.py:
Change EMAIL_HOST_USER = 'your email'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FROM_EMAIL = 'your default email'

#### static and media files:
Inside django_health project folder create media/profiles and static/images folders

