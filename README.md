# DYP Salokhenagar Alumni Portal by mee

A comprehensive web portal for DYP Salokhenagar alumni and students to connect, share achievements, post job opportunities, and communicate securely.

## Features

- **User Authentication & Roles**
  - Secure registration and login
  - Role-based access (Admin, Student, Alumni)
  - User verification system

- **Profile Management**
  - Detailed user profiles
  - Privacy controls for contact information
  - Profile visibility based on verification status

- **Posts**
  - Text-only posts for achievements and job opportunities
  - CRUD operations with permission checks
  - Categorized post listing and filtering

- **Chat System**
  - One-to-one text messaging
  - Inbox management
  - Read status tracking

- **Directory**
  - Searchable alumni and student directory
  - Filtering by role, branch, year, and name
  - Contact information visible only to verified users

- **Admin Features**
  - User verification management
  - Content moderation
  - System monitoring

## Technology Stack

- **Backend**: Django (Python)
- **Database**: SQLite (development), can be migrated to PostgreSQL/MySQL for production
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Authentication**: Django's built-in authentication system with custom extensions

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd alumni_portal
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the site at http://127.0.0.1:8000/

## Project Structure

- **accounts**: User model, authentication, and profile management
- **posts**: Achievement and job opportunity posts
- **chat**: One-to-one messaging system
- **core**: Main views, directory, and site pages

## Usage

1. Register as a student or alumni
2. Request verification from an admin
3. Once verified, access the full features of the portal:
   - View contact information of other verified users
   - Post achievements or job opportunities
   - Message other verified users
   - Update your profile information

## Admin Access

Access the admin panel at http://127.0.0.1:8000/admin/ to:
- Verify user accounts
- Manage posts and messages
- Monitor user activity

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- DYP Salokhenagar for the project requirements
- Django community for the excellent framework
- Bootstrap team for the frontend framework
