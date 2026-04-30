# Indian Constitution Learning Platform

A comprehensive Django web application for educating citizens about constitutional rights and duties through structured modules, quizzes, and community discussions.

## Features

### 🎓 Learning Modules
- Structured educational content about the Indian Constitution
- Text, images, and attachable PDF documents
- Difficulty levels (Beginner, Intermediate, Advanced)
- Estimated reading time for each module
- Created and managed by educators

### 📝 Interactive Quizzes
- Multiple-choice and true/false questions
- Automatic scoring and pass/fail evaluation
- Customizable passing score and time limits
- Maximum attempt restrictions
- Detailed answer review with explanations
- Question shuffling options

### 💬 Discussion Forums
- Community-driven discussions
- Thread creation and commenting
- Comment likes and engagement
- Module-specific discussions
- Thread pinning and status management

### 👥 Role-Based Access
- **Admin**: Manage users, content, and platform statistics
- **Educator**: Create learning modules and quizzes
- **Citizen**: Learn, take quizzes, and participate in forums

### 📊 User Dashboards
- **Admin Dashboard**: Platform overview and statistics
- **Educator Dashboard**: Content management and performance tracking
- **Citizen Dashboard**: Learning progress and quiz history

### 🔐 User Authentication
- Secure login/registration system
- Custom user model with role assignment
- Profile management with bio and profile pictures
- Email verification support

## Tech Stack

- **Backend**: Django 6.0.2 (Python)
- **Database**: SQLite 3
- **Frontend**: Django Templates + Bootstrap 5
- **Image Processing**: Pillow
- **Web Server**: Development server (Django runserver)

## Project Structure

```
constitution_platform/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── README.md                          # Project documentation
├── db.sqlite3                         # SQLite database
│
├── constitution_platform/             # Project settings
│   ├── __init__.py
│   ├── settings.py                   # Django configuration
│   ├── urls.py                       # Project-level URL routing
│   ├── asgi.py                       # ASGI configuration
│   └── wsgi.py                       # WSGI configuration
│
├── core/                              # Main application
│   ├── models.py                     # Database models
│   ├── views.py                      # View logic
│   ├── forms.py                      # Form definitions
│   ├── urls.py                       # App-level URL routing
│   ├── admin.py                      # Django admin customization
│   ├── apps.py                       # App configuration
│   ├── tests.py                      # Unit tests
│   ├── migrations/                   # Database migrations
│   └── __init__.py
│
├── templates/                         # HTML templates
│   ├── base.html                     # Base template with navbar
│   ├── core/
│   │   ├── home.html                 # Home page
│   │   ├── profile.html              # User profile
│   │   ├── edit_profile.html         # Edit profile
│   │   ├── auth/
│   │   │   ├── login.html            # Login page
│   │   │   └── register.html         # Registration page
│   │   ├── dashboard/
│   │   │   ├── admin_dashboard.html  # Admin dashboard
│   │   │   ├── educator_dashboard.html # Educator dashboard
│   │   │   └── citizen_dashboard.html  # Citizen dashboard
│   │   ├── modules/
│   │   │   ├── module_list.html      # Modules listing
│   │   │   ├── module_detail.html    # Module view
│   │   │   └── module_form.html      # Create/Edit module
│   │   ├── quizzes/
│   │   │   ├── quiz_list.html        # Quizzes listing
│   │   │   ├── quiz_detail.html      # Quiz view
│   │   │   ├── quiz_take.html        # Quiz taking interface
│   │   │   ├── quiz_result.html      # Quiz results
│   │   │   └── quiz_form.html        # Create/Edit quiz
│   │   └── discussions/
│   │       ├── thread_list.html      # Forum threads listing
│   │       ├── thread_detail.html    # Thread view with comments
│   │       └── thread_form.html      # Create/Edit thread
│
├── static/                            # Static files
│   ├── css/                          # CSS stylesheets
│   └── js/                           # JavaScript files
│
└── media/                             # User-uploaded files
    └── modules/                      # Module attachments
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- SQLite 3 (included with Python)

### Step 1: Clone/Download Project
```bash
cd "c:\Users\Lenovo\PFSD Project"
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
```
Username: admin
Email: admin@example.com
Password: (enter secure password)
```

### Step 7: Create Test Users (Optional)
You can create test users through the admin panel or use Django shell:
```bash
python manage.py shell

# In the shell:
from django.contrib.auth import get_user_model
User = get_user_model()

# Create educator user
educator = User.objects.create_user(
    username='educator1',
    email='educator@example.com',
    password='testpass123',
    role='educator',
    first_name='John',
    last_name='Educator'
)

# Create citizen user
citizen = User.objects.create_user(
    username='citizen1',
    email='citizen@example.com',
    password='testpass123',
    role='citizen',
    first_name='Jane',
    last_name='Citizen'
)

exit()
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

Server will start at: `http://127.0.0.1:8000/`

## Accessing the Application

### Public Pages
- **Home**: http://127.0.0.1:8000/
- **Modules**: http://127.0.0.1:8000/modules/
- **Quizzes**: http://127.0.0.1:8000/quizzes/
- **Forum**: http://127.0.0.1:8000/discussions/

### Authentication
- **Login**: http://127.0.0.1:8000/login/
- **Register**: http://127.0.0.1:8000/register/

### User Dashboards (Login Required)
- **Dashboard**: http://127.0.0.1:8000/dashboard/
- **Profile**: http://127.0.0.1:8000/profile/
- **Edit Profile**: http://127.0.0.1:8000/profile/edit/

### Admin Panel
- **Django Admin**: http://127.0.0.1:8000/admin/
- Login with superuser credentials

## User Roles and Permissions

### Admin (Administrator)
- Access to Django admin panel
- View all users and content
- Manage platform settings
- View statistics and analytics
- Can perform all actions

### Educator
- Create and publish learning modules
- Create quizzes with multiple questions
- View quiz statistics and student performance
- Manage their own content
- Participate in discussions

### Citizen
- Access all published learning modules
- Take quizzes and view results
- View score history and progress
- Participate in discussion forums
- Manage personal profile

## Database Models

### CustomUser
Extended Django User model with role-based access control.

**Fields:**
- `role`: admin, educator, or citizen
- `bio`: User biography
- `profile_image`: User avatar
- `is_email_verified`: Email verification status
- `created_at`, `updated_at`: Timestamps

### LearningModule
Educational content modules about constitutional aspects.

**Fields:**
- `title`, `slug`: Module identifier
- `description`, `content`: Module text
- `difficulty_level`: Beginner, Intermediate, Advanced
- `image`, `attachment`: Media files
- `status`: Draft, Published, Archived
- `created_by`: Educator who created it
- `estimated_time`: Reading time in minutes
- `created_at`, `updated_at`, `published_at`: Timestamps

### Quiz
Assessment quizzes for testing knowledge.

**Fields:**
- `title`, `description`: Quiz details
- `module`: Related learning module
- `difficulty`: Easy, Medium, Hard
- `passing_score`: Percentage required to pass
- `time_limit`: Optional time limit
- `max_attempts`: Unlimited if null
- `is_published`: Publication status
- `shuffle_questions`: Randomize order
- `show_answers`: Show after completion

### Question
Individual quiz questions.

**Fields:**
- `quiz`: Parent quiz
- `text`: Question text
- `question_type`: Multiple choice or True/False
- `explanation`: Answer explanation
- `points`: Points for correct answer
- `order`: Display order

### Choice
Answer choices for questions.

**Fields:**
- `question`: Parent question
- `text`: Choice text
- `is_correct`: Mark correct answer
- `order`: Display order

### QuizAttempt
User quiz attempts and results.

**Fields:**
- `user`, `quiz`: Relationships
- `score`, `percentage`: Results
- `is_passed`: Pass/Fail status
- `total_questions_attempted`, `total_questions_correct`: Statistics
- `time_taken`: Duration in seconds
- `started_at`, `completed_at`: Timestamps

### DiscussionThread
Forum discussion threads.

**Fields:**
- `title`, `content`: Thread details
- `author`: Creator
- `module`: Related module (optional)
- `status`: Open, Closed, Pinned
- `is_pinned`: Pin to top
- `views_count`: Number of views

### Comment
Comments on threads.

**Fields:**
- `thread`: Parent thread
- `author`: Commenter
- `content`: Comment text
- `parent`: For nested replies
- `likes_count`: Engagement metric
- `is_edited`: Modification flag

## Key Views

### Authentication Views
- `RegisterView`: User registration
- `login_view`: User login
- `logout_view`: User logout

### Dashboard Views
- `dashboard_view`: Role-based redirection
- `admin_dashboard`: Admin overview
- `educator_dashboard`: Educator content management
- `citizen_dashboard`: Citizen learning progress

### Module Views
- `ModuleListView`: Browse all modules
- `ModuleDetailView`: View module content
- `ModuleCreateView`: Create module (Educators)
- `ModuleUpdateView`: Edit module (Educators)

### Quiz Views
- `QuizListView`: Browse quizzes
- `QuizDetailView`: View quiz details
- `quiz_take_view`: Take a quiz
- `QuizResultView`: View quiz results
- `QuizCreateView`: Create quiz (Educators)

### Discussion Views
- `DiscussionThreadListView`: Browse threads
- `DiscussionThreadDetailView`: View thread with comments
- `DiscussionThreadCreateView`: Create thread
- `add_comment_view`: Post comment
- `like_comment_view`: Like comment

### Profile Views
- `profile_view`: View user profile
- `edit_profile_view`: Edit profile

## URL Patterns

### Core URLs
```
/                           → Home page
/register/                  → Registration
/login/                     → Login
/logout/                    → Logout
/dashboard/                 → Dashboard (role-based)
/profile/                   → Current user profile
/profile/<id>/              → Other user profile
/profile/edit/              → Edit profile

/modules/                   → Module listing
/modules/create/            → Create module
/modules/<slug>/            → Module detail

## MySQL Database Setup

This project uses MySQL as the primary relational database. The settings read
connection parameters from environment variables, but if `MYSQL_DATABASE` is
not defined the project falls back to the built-in SQLite file for easy
local development.

1. Install MySQL server (8.0 CE or equivalent) on your machine or a remote
   host. Create a database and user, for example using the MySQL client or
   MySQL Workbench SQL editor:

```sql
CREATE DATABASE constitution;
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'secret';
GRANT ALL PRIVILEGES ON constitution.* TO 'myuser'@'localhost';
FLUSH PRIVILEGES;
```

2. Set the following environment variables (adjust values accordingly):

```bash
export MYSQL_DATABASE=constitution
export MYSQL_USER=myuser
export MYSQL_PASSWORD=secret
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
```

For Windows PowerShell:

```powershell
$env:MYSQL_DATABASE = 'constitution'
$env:MYSQL_USER = 'myuser'
$env:MYSQL_PASSWORD = 'secret'
$env:MYSQL_HOST = 'localhost'
$env:MYSQL_PORT = '3306'
```

3. Ensure `mysqlclient` is listed in `requirements.txt` then install:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

### Connecting with MySQL Workbench

- Open MySQL Workbench and create a new **MySQL Connections** entry.
- Use the host/port and user credentials from the environment variables above.
- Click **Test Connection** to verify access. Once connected you can browse the
  `constitution` schema and run queries against it.

You can still develop without a MySQL server by omitting the variables; the
project will use SQLite.

/modules/<slug>/edit/       → Edit module

/quizzes/                   → Quiz listing
/quizzes/create/            → Create quiz
/quizzes/<id>/              → Quiz detail
/quizzes/<id>/take/         → Take quiz
/quizzes/result/<id>/       → Quiz results

/discussions/               → Forum threads
/discussions/create/        → Create thread
/discussions/<id>/          → Thread detail
/discussions/<id>/edit/     → Edit thread
/discussions/<id>/comment/  → Add comment
/comments/<id>/like/        → Like comment

/admin/                     → Django admin panel
```

## Forms

### Authentication
- `CustomUserCreationForm`: Registration
- `CustomUserChangeForm`: Profile editing

### Content
- `LearningModuleForm`: Create/edit modules
- `QuizForm`: Create/edit quizzes
- `QuestionForm`: Create questions
- `ChoiceForm`: Answer choices

### Engagement
- `DiscussionThreadForm`: Create threads
- `CommentForm`: Post comments
- `FilterModulesForm`: Filter modules

## Admin Panel Features

### CustomUserAdmin
- View users by role
- Manage user status (staff, superuser, verified)
- Filter by role and created date
- Search by username or email

### LearningModuleAdmin
- Status badges (Draft, Published, Archived)
- Filter by status and difficulty
- Auto-slug generation from title
- Media management (images, attachments)

### QuizAdmin
- Publication status display
- Question counter
- Difficulty levels
- Inline answer choices

### QuizAttemptAdmin
- Score and result display
- Pass/fail badges
- Inline answer review
- Filter by result

### DiscussionThreadAdmin
- Thread status display
- View count tracking
- Inline comments
- Thread pinning

## Static Files & Media

### CSS (Bootstrap 5)
- CDN-based Bootstrap 5 from jsDelivr
- Bootstrap Icons for UI icons
- Custom inline styles in templates

### JavaScript
- Bootstrap bundle from CDN
- Form validation
- Quiz timer functionality
- Comment like feature
- Progress tracking

### Media Management
- **Uploads**: `/media/profiles/` (user avatars)
- **Modules**: `/media/modules/` (cover images)
- **Attachments**: `/media/modules/attachments/` (PDFs)

## Email Configuration

Currently configured for development:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

For production, configure:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'app-specific-password'
```

## Security Settings

Development settings in `settings.py`:
```python
DEBUG = True
ALLOWED_HOSTS = ['*']
```

Production recommendations:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Migration Issues
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Database Locked
Remove `db.sqlite3` and run migrations again:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Future Enhancements

- [ ] Email notifications for quiz results
- [ ] User certificates upon quiz completion
- [ ] Advanced analytics dashboard
- [ ] Content recommendation engine
- [ ] Mobile application
- [ ] API (Django REST Framework)
- [ ] Real-time notifications (WebSockets)
- [ ] Content versioning system
- [ ] Social sharing capabilities
- [ ] Video content support

## Support & Documentation

- Django Documentation: https://docs.djangoproject.com/
- Bootstrap 5 Documentation: https://getbootstrap.com/docs/5.0/
- Pillow Documentation: https://pillow.readthedocs.io/

## License

This project is open source and available under the MIT License.

## Contributors

Built with ❤️ for Indian Constitution Learning

---

**Version**: 1.0.0  
**Last Updated**: February 25, 2026
"# PFSD-Project" 
