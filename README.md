# Django Portfolio Website

A modern portfolio website built with Django featuring dynamic project management through the admin interface.

## Features

- 🎨 **Dynamic Project Pages** - Each project has its own detail page
- 🔧 **Django Admin CRUD** - Add, edit, delete projects through the admin interface
- 📝 **Flexible Custom Fields** - Use JSON fields to add any custom attributes to projects
- 🖼️ **Image Upload** - Featured images for each project
- 🎯 **Publishing Control** - Publish/unpublish projects
- 📱 **Responsive Design** - Works on all devices
- 🌙 **Modern Dark Theme** - Premium gradient design with animations

## Custom Fields Examples

The `custom_fields` JSON field allows you to add any data to your projects:

```json
{
    "technologies": ["Python", "Django", "React"],
    "github_url": "https://github.com/username/repo",
    "live_url": "https://example.com",
    "gallery": ["image1.jpg", "image2.jpg"],
    "client": "Company Name",
    "duration": "3 months",
    "role": "Full Stack Developer",
    "team_size": 5,
    "highlights": [
        "Reduced load time by 40%",
        "Implemented real-time features"
    ]
}
```

## Setup Instructions

### 1. Install Dependencies

```bash
# Activate virtual environment
source .venv/bin/activate

# Install Django and Pillow (if not already installed)
pip install django pillow
```

### 2. Run Migrations

```bash
# Create migrations for the projects app
python manage.py makemigrations

# Apply migrations to create database tables
python manage.py migrate
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
# Follow the prompts to create your admin account
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit:

- **Homepage**: <http://127.0.0.1:8000/>
- **Admin**: <http://127.0.0.1:8000/admin/>

## Usage

### Adding Projects via Admin

1. Go to <http://127.0.0.1:8000/admin/>
2. Log in with your superuser credentials
3. Click on "Projects" → "Add Project"
4. Fill in the basic information (title, description, image)
5. Add custom fields in JSON format (see examples above)
6. Check "Is published" to make it visible on the site
7. Set the order number (lower numbers appear first)
8. Save!

### Custom Fields

The `custom_fields` JSON field is completely flexible. You can add:

- **technologies**: Array of tech stack items
- **github_url**: Link to GitHub repository
- **live_url**: Link to live website
- **highlights**: Array of key achievements
- **role**: Your role in the project
- **duration**: How long the project took
- **client**: Client name
- **team_size**: Number of team members
- Any other custom data you need!

## Project Structure

```bash
Portfolio/
├── manage.py
├── portfolio/              # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── projects/               # Projects app
│   ├── models.py          # Project model with JSONField
│   ├── admin.py           # Custom admin interface
│   ├── views.py           # List and detail views
│   └── urls.py
├── templates/
│   ├── base.html
│   └── projects/
│       ├── project_list.html
│       └── project_detail.html
├── static/
│   └── css/
│       └── style.css      # Modern dark theme styling
└── media/                 # Uploaded images
    └── projects/
```

## Technologies

- **Django 6.0+** - Web framework
- **Pillow** - Image handling
- **SQLite** - Database (development)
- **Custom CSS** - Modern dark theme with gradients and animations

## Next Steps

- Add more projects through the admin
- Customize the CSS in `static/css/style.css`
- Add more custom field types as needed
- Deploy to production (consider PostgreSQL for production database)

## License

MIT License - feel free to use for your portfolio!
