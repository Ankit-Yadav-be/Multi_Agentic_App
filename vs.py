import os
import base64
import requests
import streamlit as st
from pathlib import Path
import utils
from pythonenv import create_python_virtualenv
from android import create_android_project, open_android_studio

# GitHub credentials
#GITHUB_TOKEN = ''
#REPO_NAME = ""

# Function to upload file to GitHub
def upload_file_to_github(file_path):
    file_name = os.path.basename(file_path)
    github_url = f"https://api.github.com/repos/{REPO_NAME}/contents/{file_name}"
    
    with open(file_path, "rb") as file:
        content = base64.b64encode(file.read()).decode("utf-8")
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Check if file exists in repo
    response = requests.get(github_url, headers=headers)
    sha = response.json().get("sha") if response.status_code == 200 else None
    
    data = {
        "message": f"Upload {file_name}",
        "content": content,
        "branch": "main"
    }
    if sha:
        data["sha"] = sha  # Update existing file
    
    response = requests.put(github_url, headers=headers, json=data)
    
    return response.status_code == 200 or response.status_code == 201

# Set up the Streamlit page
st.set_page_config(page_title="Project Generator & GitHub File Upload", layout="wide")

# Sidebar Navigation
st.sidebar.title("🔧 Navigation")
st.sidebar.info("Use the buttons below to generate projects or upload files to GitHub.")

# Main Title
st.title("⚡ Project Generator & GitHub File Upload")
st.write("Use the following buttons to generate projects or upload files to GitHub.")

# Create two columns layout for Vite and Express
col1, col2 = st.columns(2)

with col1:
    # Generate Vite App
    if st.button("🚀 Generate Vite App", help="Generate a Vite app project"):
        with st.spinner("Generating Vite App..."):
            project_folder, zip_file = utils.create_vite_app()
            if zip_file:
                st.success("✅ Vite app created successfully!")
                with open(zip_file, "rb") as f:
                    st.download_button("📥 Download Vite Project", data=f, file_name=os.path.basename(zip_file), mime="application/zip")

    # Open in VS Code for Vite
    if st.session_state.vite_project_path:
        if st.button("🖥 Open in VS Code - Vite", help="Open Vite project in VS Code"):
            utils.open_vscode(st.session_state.vite_project_path)

with col2:
    # Generate Express Server
    include_db = st.checkbox("Include Database Connection", help="Include database connection in the server")
    include_modal = st.checkbox("Include Database Modal", help="Include database Modal in the server")
    include_api = st.checkbox("Include API Endpoints", help="Include API endpoints in the server")
    if st.button("🌐 Generate Express Server", help="Generate an Express server project"):
        with st.spinner("Generating Express Server..."):
            project_folder, zip_file = utils.create_express_server(include_db, include_api, include_modal)
            if zip_file:
                st.success("✅ Express server created successfully!")
                with open(zip_file, "rb") as f:
                    st.download_button("📥 Download Express Project", data=f, file_name=os.path.basename(zip_file), mime="application/zip")

    # Open in VS Code for Express
    if st.session_state.express_project_path:
        if st.button("🖥 Open in VS Code - Express", help="Open Express server project in VS Code"):
            utils.open_vscode(st.session_state.express_project_path)
# Android Project Section
st.markdown("---")
st.subheader("📱 Android Project")
android_project_name = st.text_input("Enter Android Project Name:", "MyAndroidApp", help="Specify your project name")

if st.button("📱 Create Android Project"):
    if not android_project_name.strip():
        st.error("❌ Please enter a valid project name.")
    else:
        with st.spinner("Creating Android Project..."):
            android_project_path = create_android_project(android_project_name)
            if android_project_path:
                st.success(f"✅ Android Project '{android_project_name}' Created at: {android_project_path}")
            else:
                st.error("❌ Failed to create Android project.")


# Python Virtual Environment Section
st.markdown("---")
st.subheader("🐍Your own ChatBot with  Python Virtual Environment")
st.write("Create a Python virtual environment for your project.")

project_name = st.text_input("Enter the project name:", help="The name of the project folder to create the virtual environment")

create_venv_button = st.button("Create Python Virtual Environment", help="Create a virtual environment for the project")

if create_venv_button:
    if not project_name:
        st.markdown("<div class='error'>Please enter a project name.</div>", unsafe_allow_html=True)
    else:
        with st.spinner(f"Creating Python virtual environment for {project_name}..."):
            project_path = create_python_virtualenv(project_name)
            if project_path:
                st.success(f"✅ Python virtual environment created at {project_path}")
                st.write(f"Project Path: {project_path}")
            else:
                st.error("❌ Failed to create virtual environment.")

# File Upload Section
st.markdown("---")
st.subheader("📂 Upload Files to GitHub")
st.write("Upload files from your local folder directly to your GitHub repository.")

folder = st.text_input("Enter folder path to upload files:", key="folder_path", help="Path of the folder to upload from")

upload_button = st.button("Upload Files", help="Upload all files from the selected folder to GitHub")

if upload_button:
    if not folder:
        st.markdown("<div class='error'>Please enter a folder path.</div>", unsafe_allow_html=True)
    else:
        folder_path = Path(folder)
        if folder_path.exists() and folder_path.is_dir():
            files = list(folder_path.glob("*"))
            progress = st.progress(0)
            success_count = 0
            file_upload_status = {}  # Store status of each file upload
            
            for i, file in enumerate(files):
                if file.is_file():
                    file_name = file.name
                    file_status = f"Uploading {file_name}..."
                    file_upload_status[file_name] = file_status
                    progress.progress((i + 1) / len(files))
                    
                    if upload_file_to_github(str(file)):
                        success_count += 1
                        file_upload_status[file_name] = f"✅ {file_name} uploaded successfully!"
                    else:
                        file_upload_status[file_name] = f"❌ Failed to upload {file_name}"
            
            # Display file upload status
            for file_name, status in file_upload_status.items():
                st.text(status)
            
            st.markdown(f"<div class='success'>✅ {success_count}/{len(files)} files uploaded successfully!</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='error'>Invalid folder path! Please check and try again.</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.text("Created by Ankit Yadav | © 2025")
