---
description: Initial configuration
globs: 
---
# Instructions

This document provides a step-by-step guide for setting up the **twitterclone** project using the following stack:

- **Python**
- **Poetry** (for dependency management)
- **Django** with **Django Rest Framework** and **Django Templates**
- **Bootstrap** (via CDN)
- **Django Crispy Forms**
- **HTMX** and **Alpine.js** (via CDN and optionally using django-htmx)
- **Docker** (with Dockerfile and docker-compose for local testing)
- **PostgreSQL** (via psycopg2-binary, as defined in the dependencies)
- **Deployment** via Railway (using Gunicorn and Whitenoise)

---

## 1. Create and Activate a Virtual Environment

Although Poetry can manage virtual environments automatically, you can also create one manually if preferred.

### Create the virtual environment

- **python -m venv env**

### Activate the environment on Windows:

- **env\Scripts\activate**

---

## 2. Install Dependencies from requirements.txt

If you wish to install dependencies from your existing requirements.txt from a previous project, run:

### Install

- **pip install -r requirements.txt**

Note: This step is optional if you plan to migrate all dependencies into your Poetry-managed project.

---

## 3. Configure the pyproject.toml and Install Dependencies via Poetry

If you already have a pyproject.toml (from your "bookstore" project), modify the metadata (such as the project name, version, and description) as needed for twitterclone. For example:

### pyproject.toml

```
[tool.poetry]
name = "twitterclone"
version = "0.1.0"
description = "A simple Twitter clone using Django and DRF"
authors = ["Rodrigo Cinelli <rodcinelli@gmail.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = ">=3.12"
black = "^24.10.0"
factory-boy = "^3.3.1"
pytest = "^8.3.4"
django = "^5.1.4"
djangorestframework = "^3.15.2"
django-extensions = "^3.2.3"
django-debug-toolbar = "^5.0.1"
psycopg2-binary = "^2.9.10"
flake8 = "^7.1.1"
whitenoise = "^6.8.2"
gunicorn = "^23.0.0"

[tool.poetry.group.dev.dependencies]
black = "^24.10.0"
pytest = "^8.3.4"
factory-boy = "^3.3.1"

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

Note:

If you already have a pyproject.toml, there is no need to run poetry init --no-interaction since that command is only used to create a new one from scratch.

Once the file is updated, install the dependencies with:

- **poetry install**

---

## 4. Add Additional Dependencies for the Project

Add the packages specific to the twitterclone project that are not present in your current pyproject.toml:

### Add Django Crispy Forms

- **poetry add django-crispy-forms**

Then update your settings.py with the appropriate configuration (e.g., set CRISPY_TEMPLATE_PACK = 'bootstrap5' or your preferred version).

### Optionally, Add django-htmx for Better HTMX Integration

- **poetry add django-htmx**

Remember to add 'django_htmx' to your INSTALLED_APPS in settings.py if you use this package.

---

## 5. Front End Assets via CDN

Since Bootstrap, HTMX, and Alpine.js are JavaScript/CSS libraries, you can include them via CDN in your base template. For example, add the following in your base HTML template:

### HTML 

**1. Bootstrap CSS** 

```
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
```

**2. HTMX**

```
<script src="https://unpkg.com/htmx.org@1.9.2"></script>
```

**3. Alpine.js**

```
<script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
```

---

## 6. Set Up the Django Project Structure

It is a good practice to organize your project code in a dedicated source folder (e.g., src/). This helps keep your repository organized and separates application code from configuration files.

### Create a src Directory and Start the Django Project

On the root of the project:

- **django-admin startproject twitterclone src/twitterclone**

### Notes on Using src:

Placing your Django project in a src folder helps maintain a clear separation between your application code and other project files.

If your previous project (e.g., "bookstore") had apps created in the root, be sure to update any path references (such as BASE_DIR in settings.py) accordingly.

This structure minimizes conflicts when managing multiple projects in one repository.

--- 

## 7. Docker Configuration

Assuming you already have a Dockerfile and a docker-compose.yml, ensure they are updated to match your new project structure.

### Note: 

If you are migrating your project from "bookstore" to "twitterclone", be sure to update the Gunicorn command's WSGI module (currently bookstore.wsgi:application) to match your new project (for example, twitterclone.wsgi:application).

### To build and run the containers, execute:

- **docker-compose up --build**













