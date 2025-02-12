import os
import subprocess

# Function to create Flask project
def create_flask_project(project_name):
    try:
        # Create project folder structure
        os.makedirs(f"{project_name}/app", exist_ok=True)
        os.makedirs(f"{project_name}/instance", exist_ok=True)

        # Create basic files
        with open(f"{project_name}/app/__init__.py", "w") as f:
            f.write('from flask import Flask\n\napp = Flask(__name__)\n\n')

        with open(f"{project_name}/instance/config.py", "w") as f:
            f.write('SECRET_KEY = "your_secret_key"\n')

        with open(f"{project_name}/run.py", "w") as f:
            f.write('from app import app\n\nif __name__ == "__main__":\n    app.run(debug=True)\n')

        # Install Flask
        subprocess.run(["pip", "install", "flask"], check=True)

        return f"Flask project '{project_name}' created successfully!"
    except Exception as e:
        return f"Error: {e}"

# Function to create Django project
def create_django_project(project_name):
    try:
        # Install Django
        subprocess.run(["pip", "install", "django"], check=True)

        # Create Django project using Django's startproject command
        subprocess.run(["django-admin", "startproject", project_name], check=True)

        return f"Django project '{project_name}' created successfully!"
    except Exception as e:
        return f"Error: {e}"
