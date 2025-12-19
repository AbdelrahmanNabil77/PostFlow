
# PostFlow blogging platform API

A robust and feature-rich RESTful API for a modern blogging platform built with Django and Django REST Framework. This API provides full CRUD operations for blog posts, user management, advanced filtering, and secure authentication.

## 🚀 Live API

**Base URL:**  `https://AbdElRahmanNabil.pythonanywhere.com`

## 📋 Table of Contents

-   Features
    
-   Technology Stack
    
-   Quick Start
    
-   Authentication
    
-   API Endpoints
    
-   Filtering & Search
    
-   Examples
    
-   Deployment
    
-   Testing
    

## ✨ Features

### Core Features

-   ✅ **User Authentication** - JWT-based secure authentication
    
-   ✅ **Blog Post CRUD** - Create, Read, Update, Delete blog posts
    
-   ✅ **Advanced Filtering** - Filter by category, author, tags, date ranges
    
-   ✅ **Full-Text Search** - Search across titles, content, and tags
    
-   ✅ **Pagination** - Efficient handling of large datasets
    
-   ✅ **Draft System** - Save posts as drafts before publishing
    
-   ✅ **Permissions** - Users can only edit their own posts
    

### Advanced Features

-   🔒 **Role-based permissions** (Admin, Author, Reader)
    
-   🏷️ **Tag management** and categorization
    
-   ⭐ **Featured posts** highlighting
    

## 🛠 Technology Stack

-   **Backend Framework:** Django 4.2, Django REST Framework
    
-   **Authentication:** JWT (JSON Web Tokens)
    
-   **Database:** SQLite (Development), PostgreSQL (Production)
    
-   **Deployment:** PythonAnywhere
   
    

## 🚦 Quick Start

### Prerequisites

-   Python 3.8+
    
-   pip package manager
    
-   Git
    

### Installation

bash

# Clone the repository
git clone <repository-url>
cd PostFlow

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. All protected endpoints require a valid token in the Authorization header.

### Getting Started with Authentication

1.  **Register a new user:**
    

bash

curl -X POST https://AbdElRahmanNabil.pythonanywhere.com/api/accounts/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123",
    "password2": "SecurePass123"
  }'

2.  **Login to get tokens:**
    

bash

curl -X POST https://AbdElRahmanNabil.pythonanywhere.com/api/accounts/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123"
  }'

**Response:**

json

{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}

3.  **Use the access token:**
    

bash

curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  https://AbdElRahmanNabil.pythonanywhere.com/api/blog/posts/

4.  **Refresh expired tokens:**
    

bash

curl -X POST https://AbdElRahmanNabil.pythonanywhere.com/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN"
  }'

## 📡 API Endpoints

### Authentication Endpoints



## 🔐 Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/accounts/auth/register/` | Register new user | No |
| POST | `/api/accounts/auth/login/` | Login user | No |
| POST | `/api/accounts/auth/logout/` | Logout user | Yes |
| POST | `/api/token/` | Get JWT tokens | No |
| POST | `/api/token/refresh/` | Refresh access token | No |

## 👤 User Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/accounts/profile/` | Get user profile | Yes |
| PUT | `/api/accounts/profile/update_profile/` | Update profile | Yes |
| GET | `/api/blog/users/` | List all users | Admin only |
| GET | `/api/blog/users/{username}/` | Get user details | Yes |


## 📝 Blog Posts

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/blog/posts/` | List all posts | No |
| POST | `/api/blog/posts/` | Create new post | Yes |
| GET | `/api/blog/posts/{id}/` | Get post details | No |
| PUT | `/api/blog/posts/{id}/` | Update post | Owner only |
| PATCH | `/api/blog/posts/{id}/` | Partial update | Owner only |
| DELETE | `/api/blog/posts/{id}/` | Delete post | Owner only |
| POST | `/api/blog/posts/{id}/publish/` | Publish draft | Owner only |
| GET | `/api/blog/posts/featured/` | Get featured posts | No |
| GET | `/api/blog/posts/popular/` | Get popular posts | No |
| GET | `/api/blog/posts/by_category/` | Filter by category | No |
| GET | `/api/blog/posts/by_author/` | Filter by author | No |


## 🗂 Categories

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/blog/categories/` | List all categories | No |
| POST | `/api/blog/categories/` | Create category | Admin only |
| GET | `/api/blog/categories/{id}/` | Get category details | No |
| PUT | `/api/blog/categories/{id}/` | Update category | Admin only |
| DELETE | `/api/blog/categories/{id}/` | Delete category | Admin only |


## 🏷 Tags

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/blog/tags/` | List all tags | No |
| POST | `/api/blog/tags/` | Create tag | Admin only |
| GET | `/api/blog/tags/{id}/` | Get tag details | No |
| PUT | `/api/blog/tags/{id}/` | Update tag | Admin only |
| DELETE | `/api/blog/tags/{id}/` | Delete tag | Admin only |

## 🔍 Filtering & Search

### Basic Filtering

Filter posts using query parameters:

bash

# Filter by category
GET /api/blog/posts/?category=technology

# Filter by author
GET /api/blog/posts/?author=johndoe

# Filter by status
GET /api/blog/posts/?status=published

# Filter by featured
GET /api/blog/posts/?is_featured=true

# Multiple filters
GET /api/blog/posts/?category=technology&author=johndoe&is_featured=true

### Date Range Filtering

bash

# Posts published after a specific date
GET /api/blog/posts/?published_date_after=2024-01-01

# Posts published before a specific date
GET /api/blog/posts/?published_date_before=2024-12-31

# Date range
GET /api/blog/posts/?published_date_after=2024-01-01&published_date_before=2024-06-30

### Advanced Search

bash

# Full-text search across multiple fields
GET /api/blog/posts/?q=django+tutorial

# Search with specific fields
GET /api/blog/posts/?title__icontains=django&content__icontains=rest+api

# Tag-based filtering
GET /api/blog/posts/?tag_names=python,web+development

### Sorting

bash

# Sort by published date (newest first)
GET /api/blog/posts/?ordering=-published_date

# Sort by view count (most popular first)
GET /api/blog/posts/?ordering=-view_count

# Sort by title (alphabetical)
GET /api/blog/posts/?ordering=title

# Multiple sorting
GET /api/blog/posts/?ordering=-view_count,-published_date

### Pagination

bash

# Get first page (10 items per page default)
GET /api/blog/posts/?page=1

# Custom page size
GET /api/blog/posts/?page=1&page_size=20

# Get specific page
GET /api/blog/posts/?page=3

**Pagination Response Format:**

json

{
  "links": {
    "next": "https://AbdElRahmanNabil.pythonanywhere.com/api/blog/posts/?page=2",
    "previous": null
  },
  "count": 150,
  "total_pages": 15,
  "current_page": 1,
  "results": [
    // post data...
  ]
}

## 📝 Examples

### Create a Blog Post

bash

curl -X POST https://AbdElRahmanNabil.pythonanywhere.com/api/blog/posts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Getting Started with Django REST Framework",
    "content": "Django REST Framework is a powerful toolkit for building Web APIs...",
    "category": 1,
    "tags": ["django", "api", "rest"],
    "status": "draft"
  }'

### Update a Post

bash

curl -X PATCH https://AbdElRahmanNabil.pythonanywhere.com/api/blog/posts/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "status": "published"
  }'

### Publish a Draft

bash

curl -X POST https://AbdElRahmanNabil.pythonanywhere.com/api/blog/posts/1/publish/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

### Get Posts by Category

bash

curl -X GET https://AbdElRahmanNabil.pythonanywhere.com/api/blog/posts/by_category/?category=Technology

### Search Posts

bash

curl -X GET "https://AbdElRahmanNabil.pythonanywhere.com/api/blog/posts/?q=django%20tutorial&ordering=-published_date&page=1"

## 🚢 Deployment

### Deploying to PythonAnywhere

1.  **Create a PythonAnywhere account** at [pythonanywhere.com](https://www.pythonanywhere.com/)
    
2.  **Upload your code:**
    
    bash
    
    # From your local machine
    git push origin main
    
    # On PythonAnywhere console
    git clone <your-repository-url>
    
3.  **Create a virtual environment:**
    
    bash
    
    mkvirtualenv --python=/usr/bin/python3.8 blog-api
    pip install -r requirements.txt
    
4.  **Configure Web App:**
    
    -   Go to Web tab
        
    -   Click "Add a new web app"
        
    -   Choose "Manual configuration"
        
    -   Select Python 3.8
        
    -   Enter path to your WSGI file
        
5.  **Update WSGI file:**
    
    python
    
    import os
    import sys
    
    path = '/home/AbdElRahmanNabil/blogging-platform-api'
    if path not in sys.path:
        sys.path.append(path)
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'
    
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
6.  **Set up environment variables:**
    
    bash
    
    # Create .env file in your home directory
    echo "DEBUG=False" >> /home/AbdElRahmanNabil/.env
    echo "SECRET_KEY=your-secret-key" >> /home/AbdElRahmanNabil/.env
    echo "DATABASE_URL=mysql://..." >> /home/AbdElRahmanNabil/.env
    
7.  **Run migrations:**
    
    bash
    
    python manage.py migrate
    
8.  **Collect static files:**
    
    bash
    
    python manage.py collectstatic
    
9.  **Restart your web app**


## 📊 Database Schema

text

User
├── id (PK)
├── username
├── email
├── password
└── date_joined

Category
├── id (PK)
├── name
├── description
└── created_at

Tag
├── id (PK)
├── name
└── created_at

BlogPost
├── id (PK)
├── title
├── content
├── author_id (FK → User)
├── category_id (FK → Category)
├── published_date
├── created_at
├── updated_at
├── status (draft/published)
├── view_count
├── is_featured
└── tags (M2M → Tag)
