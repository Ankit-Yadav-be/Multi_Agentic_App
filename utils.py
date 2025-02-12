import subprocess
import shutil
import os
import zipfile
import streamlit as st

# ✅ VS Code का सही Path डालें:
VSCODE_PATH = r"C:\Users\ay870\AppData\Local\Programs\Microsoft VS Code\Code.exe"

# ✅ Streamlit Session State (Global Variable for Project Paths)
if "vite_project_path" not in st.session_state:
    st.session_state.vite_project_path = None

if "express_project_path" not in st.session_state:
    st.session_state.express_project_path = None

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

        st.success("✅ C++ (MinGW) installed and environment variables set successfully!")
    except Exception as e:
        st.error(f"❌ Error installing C++ or setting environment variables: {e}")

# Create Vite app
def create_vite_app():
    project_name = "my-vite-app"
    desktop_path = os.path.join(os.path.expanduser("~"), "OneDrive\\Desktop")
    project_path = os.path.join(desktop_path, project_name)
    
    if os.path.exists(project_path):
        shutil.rmtree(project_path)
    
    try:
        os.chdir(desktop_path)
        subprocess.run([r"C:\\Program Files\\nodejs\\npx.cmd", "create-vite@latest", project_name, "--template", "react"], check=True)
        st.session_state.vite_project_path = project_path  # ✅ Store Path Globally
        return project_path, zip_project(project_path)
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Error creating Vite app: {e}")
        return None, None

# Create Express Server
def create_express_server(include_db, include_api, include_modal):
    project_name = "express-server"
    desktop_path = os.path.join(os.path.expanduser("~"), "OneDrive\\Desktop")
    project_path = os.path.join(desktop_path, project_name)
    
    if os.path.exists(project_path):
        shutil.rmtree(project_path)
    
    try:
        os.mkdir(project_path)
        os.chdir(project_path)
        subprocess.run([r"C:\\Program Files\\nodejs\\npm.cmd", "init", "-y"], check=True)
        subprocess.run([r"C:\\Program Files\\nodejs\\npm.cmd", "install", "express", "cors", "dotenv", "morgan"], check=True)
        
        with open(os.path.join(project_path, "server.js"), "w", encoding="utf-8") as f:
            f.write(''' 
require("dotenv").config();
const express = require("express");
const cors = require("cors");
const morgan = require("morgan");
const app = express();
app.use(express.json());
app.use(cors());
app.use(morgan("dev"));

app.get("/", (req, res) => {
    res.send("Hello from Express Server!");
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
''')

        if include_db:
            with open(os.path.join(project_path, "db.js"), "w", encoding="utf-8") as f:
                f.write(''' 
const mongoose = require("mongoose");

const connectDB = async () => {
    try {
        await mongoose.connect(process.env.MONGO_URI, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });
        console.log("MongoDB connected successfully");
        st.success("✅ MongoDB connected successfully!");  # This line will show the success message in Streamlit
    } catch (error) {
        console.error("MongoDB connection failed", error);
        st.error("❌ MongoDB connection failed: " + error.message);  # Show error message if connection fails
        process.exit(1);
    }
};

module.exports = connectDB;
''')

            # Display success message after the database setup
            st.success("✅ Database created successfully!")
            with open(os.path.join(project_path, ".env"), "w", encoding="utf-8") as f:
                f.write("MONGO_URI=your_mongodb_connection_string_here")

        # Include API Endpoints if Selected
        if include_api:
            result = create_express_api_endpoints(project_path)
            st.success(result)
        if include_modal:
            result = create_db_models(project_path)
            st.success(result)    

        st.session_state.express_project_path = project_path  # ✅ Store Path Globally
        return project_path, zip_project(project_path)
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Error creating Express server: {e}")
        return None, None

# Database Models
def create_db_models(project_path):
    """Function to create database models."""
    models_path = os.path.join(project_path, "models")
    os.makedirs(models_path, exist_ok=True)
    
    # Example of a User model
    with open(os.path.join(models_path, "modals.js"), "w", encoding="utf-8") as f:
        f.write(''' 
const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
    },
    email: {
        type: String,
        required: true,
        unique: true,
    },
    password: {
        type: String,
        required: true,
    },
    isAdmin: {
        type: Boolean,
        default: false,
    },
}, { timestamps: true });

const User = mongoose.model("User", userSchema);
module.exports = User;
''')
    
    # You can add more models here (like Product, Order, etc.)

    return "✅ Database model created successfully!"

# Zip Project Files
def zip_project(project_path):
    zip_path = project_path + ".zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(project_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), project_path))
    return zip_path

# Create Express API Endpoints
def create_express_api_endpoints(project_path):
    api_code = '''
const express = require("express");
const router = express.Router();

// Sample endpoint
router.get("/test", (req, res) => {
    res.json({ message: "API is working!" });
});

module.exports = router;
'''
    try:
        api_path = os.path.join(project_path, "routes")
        os.makedirs(api_path, exist_ok=True)
        
        with open(os.path.join(api_path, "api.js"), "w") as f:
            f.write(api_code)

        # Add API routes to server.js
        server_path = os.path.join(project_path, "server.js")
        with open(server_path, "a", encoding="utf-8") as f:
            f.write('\nconst apiRoutes = require("./routes/api");\napp.use("/api", apiRoutes);\n')

        return "✅ API endpoints added successfully!"
    except Exception as e:
        return f"❌ Error creating API endpoints: {e}"

# Open VS Code with the Project
def open_vscode(project_path):
    if project_path and os.path.exists(project_path):
        if os.path.exists(VSCODE_PATH):
            try:
                subprocess.Popen([VSCODE_PATH, project_path], shell=True)
                st.success("✅ VS Code Opened Successfully!")
            except Exception as e:
                st.error(f"❌ Error Opening VS Code: {e}")
        else:
            st.error("❌ VS Code path गलत है! सही path चेक करें।")
    else:
        st.error("❌ पहले प्रोजेक्ट बनाएं, फिर VS Code खोलें.")
