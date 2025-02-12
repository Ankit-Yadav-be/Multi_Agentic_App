import subprocess
import os

# ✅ Android Studio ka correct path update karein
ANDROID_STUDIO_PATH = r"C:\Program Files\Android\Android Studio\bin\studio64.exe"

def get_desktop_path():
    """User ke Desktop ka path return karega."""
    return os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")

def create_android_project(project_name):
    """Naya Android Studio project create karta hai ya existing project open karta hai."""
    if not project_name.strip():
        print("❌ Invalid project name! Please enter a valid name.")
        return None
    
    project_path = os.path.join(get_desktop_path(), project_name)

    if os.path.exists(project_path):
        print("⚠ Project already exists! Opening in Android Studio...")
        open_android_studio(project_path)
        return project_path

    try:
        os.makedirs(project_path, exist_ok=True)
        subprocess.run([ANDROID_STUDIO_PATH, project_path], check=True)
        print(f"✅ Android Studio Project Created at: {project_path}")
        return project_path
    except FileNotFoundError:
        print("❌ Android Studio not found! Please check the path.")
    except subprocess.CalledProcessError:
        print("❌ Failed to open Android Studio! Ensure it's installed properly.")
    except Exception as e:
        print(f"❌ Error Creating Android Project: {e}")

    return None

def open_android_studio(project_path):
    """Existing Android Studio project ko open karta hai."""
    if not project_path or not os.path.exists(project_path):
        print("❌ Project not found! Create a project first.")
        return

    try:
        subprocess.Popen([ANDROID_STUDIO_PATH, project_path], shell=True)
        print("✅ Android Studio Opened Successfully!")
    except FileNotFoundError:
        print("❌ Android Studio path incorrect! Update the correct path.")
    except Exception as e:
        print(f"❌ Error Opening Android Studio: {e}")

# ✅ Example Usage
if __name__ == "__main__":
    project_name = input("Enter Android Project Name: ").strip()
    if project_name:
        create_android_project(project_name)
    else:
        print("❌ Please enter a valid project name.")
