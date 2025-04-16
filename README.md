# Baptism Management System

## Overview

The **Baptism Management System** is a web-based application designed to streamline the management of baptism records for parishes. It provides functionality for secretaries, priests, and users to manage and access baptism-related data efficiently. The system includes features such as user registration, login, baptism record management, dashboards, and advanced functionalities like email notifications, QR code generation for certificate verification, and PDF downloads.

---

## Features

### 1. User Roles
- **Secretary**: Responsible for managing baptism records, including adding, editing, and approving baptisms.
- **Priest**: Can view baptism records specific to their parish.
- **User**: Can register and log in to access baptism-related services.

### 2. Authentication
- Secure login and registration for secretaries, priests, and users.
- "Remember this Device" functionality for persistent login sessions.

### 3. Baptism Records
- Add, edit, and manage baptism records.
- Fields include:
  - Child's name
  - Date and time of baptism
  - Parents' names
  - Godparents' names
  - Contact information
  - Status (Pending, Approved, Rejected)

### 4. Dashboards
- **Priest Dashboard**: Displays baptism records for the priest's parish.
- **Secretary Dashboard**: Allows secretaries to manage baptism records and view statistics.

### 5. Validation
- Server-side and client-side validation for fields like contact numbers, email addresses, and required fields.

### 6. Pagination
- Baptism records are paginated for better usability when dealing with large datasets.

### 7. Responsive Design
- The application is designed to work seamlessly on desktops, tablets, and mobile devices.

### 8. Automatic Email Notifications
- Sends automatic email notifications to parents and godparents after a baptism record is approved.
- Email templates can be customized for different events.

### 9. QR Code for Certificate Verification
- Generates a QR code for each baptism certificate.
- The QR code can be scanned to verify the authenticity of the certificate.

### 10. PDF Downloads
- Allows users to download baptism certificates as PDF files.
- Certificates include all relevant details, including the QR code for verification.

---

## Project Structure

### Key Files and Directories

- **templates/**: Contains all HTML templates for the application.
  - `secretary_login.html`
  - `priest_dashboard.html`
  - `baptism_form.html`
  - `question_list.html`

- **baptism/models.py**: Defines the database models, including `Baptism`, `LoginDetails`, and `ParishDetails`.

- **baptism/forms.py**: Contains Django forms for handling user input and validation.

- **baptism/views.py**: Contains the logic for handling requests and rendering templates.

- **baptism/static/**: Contains static assets like CSS, JavaScript, and images.

- **baptism/utils.py**: Contains utility functions for generating QR codes, sending emails, and creating PDFs.

---

## Installation and Setup

### Prerequisites
- Python 3.x
- Django 4.x
- A database (SQLite is used by default)

### Steps

```bash
# Clone the Repository
git clone https://github.com/yourusername/baptism-management-system.git
cd baptism-management-system

# Install Dependencies
pip install -r requirements.txt

# Apply Migrations
python manage.py migrate

# Run the Development Server
python manage.py runserver
