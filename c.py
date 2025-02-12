import subprocess
import os

# Install C++ (MinGW) and set environment variable
def install_cpp_and_set_env():
    try:
        # Download MinGW installer
        mingw_installer_url = "https://sourceforge.net/projects/mingw-w64/files/latest/download"
        installer_path = os.path.join(os.path.expanduser("~"), "Downloads", "mingw-installer.exe")
        subprocess.run(["curl", "-L", mingw_installer_url, "-o", installer_path], check=True)

        # Run the installer (we can include specific options if needed)
        subprocess.run([installer_path, "/S"], check=True)

        # Set Environment Variable
        mingw_bin_path = os.path.join(os.path.expanduser("~"), "mingw", "bin")  # Adjust according to MinGW installation
        os.environ["PATH"] += os.pathsep + mingw_bin_path
        
        # Add the path to System Environment Variables (permanent)
        subprocess.run(f'setx PATH "%PATH%;{mingw_bin_path}"', shell=True)

        return "✅ C++ (MinGW) installed and environment variables set successfully!"
    except Exception as e:
        return f"❌ Error installing C++ or setting environment variables: {e}"
