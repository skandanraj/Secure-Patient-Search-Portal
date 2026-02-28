"""
================================================================================
Healthcare UHID Secure Search Dashboard
--------------------------------------------------------------------------------
Author      : Skanda N Raj
Tech Stack  : Python, Gradio, Pandas, Bcrypt
Purpose     : Secure internal healthcare dashboard to search and filter
              patient appointment records using UHID.

Project Highlights:
- Role-based login authentication using bcrypt password hashing
- Session timeout management (60 mins)
- Activity logging (login, logout, search tracking)
- Multi-filter search (UHID, Hospital, Speciality)
- Excel export functionality
- Secure configuration using environment variables (.env)
- LAN deployment supported

Security Features:
- No hardcoded credentials
- Environment-based configuration
- Password hashing with bcrypt
- Session expiration handling
- Activity audit logging

Deployment:
- Localhost
- LAN (same WiFi network)
- Can be deployed to cloud (HuggingFace / Render / AWS)

NOTE:
This project uses a dummy dataset for GitHub demonstration.
No real patient data is included.

================================================================================
"""

import gradio as gr
import pandas as pd
from pathlib import Path
import socket
import bcrypt
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# ================== LOAD ENV VARIABLES ==================
load_dotenv()

# ================== CONFIGURATION ==================
# Excel file path (stored in .env for security)
EXCEL_PATH = Path(os.getenv("EXCEL_PATH", "data/MIS_Report.xlsx"))

# Activity log file
LOG_PATH = Path("user_activity_log.csv")

# Secure user credentials (loaded from environment variables)
VALID_USERS = {
    "admin": bcrypt.hashpw(os.getenv("ADMIN_PASSWORD", "admin123").encode('utf-8'), bcrypt.gensalt()),
    "skanda": bcrypt.hashpw(os.getenv("SKANDA_PASSWORD", "skanda123").encode('utf-8'), bcrypt.gensalt()),
    "sanish": bcrypt.hashpw(os.getenv("SANISH_PASSWORD", "sanish123").encode('utf-8'), bcrypt.gensalt()),
}

# Session timeout (in seconds)
SESSION_TIMEOUT = 3600  # 60 minutes
active_sessions = {}

# Columns to display in dashboard
DISPLAY_COLUMNS = [
    "UHID", "Patient Name", "Appointment ID", "Appointment Date",
    "Appointment Time", "Procedure", "Hospital Name", "Speciality",
    "Doctor Name", "Appt. Payment Status", "Appt. Status",
    "Booked DateTime", "Booked_Time", "HIS Invoice No.", "Invoice No",
    "Payment Reference No.", "Payment Type", "Consultation DateTime",
    "Completed DateTime", "Cancelled Datetime", "Refund Amount (₹)"
]

# ================== ACTIVITY LOG FUNCTION ==================
def log_activity(username, action, details=""):
    """
    Logs user activity into CSV file for audit tracking.
    Tracks login, logout, failed login, and search actions.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = pd.DataFrame([{
        "Timestamp": timestamp,
        "Username": username,
        "Action": action,
        "Details": details
    }])

    if LOG_PATH.exists():
        log_entry.to_csv(LOG_PATH, mode='a', index=False, header=False)
    else:
        log_entry.to_csv(LOG_PATH, index=False, header=True)

# ================== LOAD DATA ==================
def load_data():
    """
    Loads Excel data safely.
    Returns error dataframe if file fails to load.
    """
    try:
        df = pd.read_excel(EXCEL_PATH)
        df.columns = [col.strip() for col in df.columns]
        return df
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})

data = load_data()

# ================== SEARCH FUNCTION ==================
def search_uhid(uhid, hospital, speciality, username):
    """
    Core search logic.
    Filters data based on:
    - UHID (partial match supported)
    - Hospital Name
    - Speciality
    """
    if username not in active_sessions or (time.time() - active_sessions[username] > SESSION_TIMEOUT):
        return pd.DataFrame(), "⏰ Session expired. Please log in again."

    active_sessions[username] = time.time()

    if data.empty or "Error" in data.columns:
        return pd.DataFrame(), "❌ Error loading Excel file."

    df = data.copy()

    if hospital != "All":
        df = df[df["Hospital Name"] == hospital]

    if speciality != "All":
        df = df[df["Speciality"] == speciality]

    if uhid:
        df = df[df["UHID"].astype(str).str.contains(uhid, case=False, na=False)]

    df = df[[c for c in DISPLAY_COLUMNS if c in df.columns]]

    if df.empty:
        log_activity(username, "Search", "No results")
        return pd.DataFrame(), "⚠️ No matching UHID found."
    else:
        df.to_excel("search_results.xlsx", index=False)
        log_activity(username, "Search", f"Results={len(df)}")
        return df, f"✅ Showing {len(df)} matching records."

# ================== DROPDOWN LISTS ==================
hospital_list = ["All"] + sorted(data["Hospital Name"].dropna().unique().tolist()) if "Hospital Name" in data.columns else ["All"]
speciality_list = ["All"] + sorted(data["Speciality"].dropna().unique().tolist()) if "Speciality" in data.columns else ["All"]

# ================== GRADIO APP ==================
with gr.Blocks(theme=gr.themes.Soft(primary_hue="red")) as app:

    # LOGIN PAGE
    with gr.Group(visible=True) as login_page:
        gr.Markdown("## 🏥 Healthcare UHID Secure Dashboard")
        username = gr.Textbox(label="Username")
        password = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Sign In")
        login_msg = gr.Markdown("")

    # DASHBOARD PAGE
    with gr.Group(visible=False) as dashboard_page:
        gr.Markdown("## 🔎 UHID Search Dashboard")
        logout_btn = gr.Button("Logout")

        uhid_input = gr.Textbox(label="Enter UHID")
        hospital_dropdown = gr.Dropdown(label="Hospital Name", choices=hospital_list, value="All")
        speciality_dropdown = gr.Dropdown(label="Speciality", choices=speciality_list, value="All")

        search_button = gr.Button("Search")
        result_msg = gr.Markdown("")
        result_table = gr.DataFrame(visible=False)
        download_btn = gr.File(visible=False)

    def on_search(uhid, hospital, speciality, username):
        df, msg = search_uhid(uhid, hospital, speciality, username)
        if not df.empty:
            return (
                gr.update(value=df, visible=True),
                msg,
                gr.update(value="search_results.xlsx", visible=True)
            )
        else:
            return (
                gr.update(visible=False),
                msg,
                gr.update(visible=False)
            )

    search_button.click(
        on_search,
        inputs=[uhid_input, hospital_dropdown, speciality_dropdown, username],
        outputs=[result_table, result_msg, download_btn]
    )

    def logout_user(username):
        if username in active_sessions:
            del active_sessions[username]
        log_activity(username, "Logout")
        return (
            gr.update(visible=True),
            gr.update(visible=False),
            "",
            "",
        )

    logout_btn.click(
        logout_user,
        inputs=[username],
        outputs=[login_page, dashboard_page, username, password]
    )

    def verify_login(user, pwd):
        if user in VALID_USERS and bcrypt.checkpw(pwd.encode('utf-8'), VALID_USERS[user]):
            active_sessions[user] = time.time()
            log_activity(user, "Login")
            return (
                gr.update(visible=False),
                gr.update(visible=True),
                "",
            )
        else:
            log_activity(user, "Failed Login")
            return (
                gr.update(visible=True),
                gr.update(visible=False),
                "❌ Invalid credentials"
            )

    login_btn.click(
        verify_login,
        inputs=[username, password],
        outputs=[login_page, dashboard_page, login_msg]
    )

# ================== LOCAL HOSTING ==================
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print(f"\nDashboard running at: http://127.0.0.1:7860")
print(f"LAN access: http://{local_ip}:7860\n")

app.launch(server_name="0.0.0.0", server_port=7860)
