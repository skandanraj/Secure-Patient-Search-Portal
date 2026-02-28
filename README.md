# 🏥 Healthcare UHID Secure Dashboard  

---

## 📌 Project Overview

During my internship at **Aster DM Healthcare**, the operational team frequently contacted the MIS team to retrieve patient appointment details, UHID-based records, hospital-level data, and payment information.

This repetitive manual process created operational delays and unnecessary dependency on the MIS team.

To solve this problem, I developed a **secure internal UHID Search Dashboard** using Python and Gradio that enabled the operations team to independently search, filter, and download required data over the internal LAN network.

This system reduced manual effort and improved operational efficiency.

---

## 🎯 Problem Statement

Before this solution:

- Operational team depended on MIS for repeated data extraction  
- Manual Excel filtering was time-consuming  
- Frequent ad-hoc requests reduced productivity  
- No centralized self-service data access system  

The team required:

- Quick UHID-based search  
- Hospital & speciality filtering  
- Payment & invoice tracking  
- Exportable reports  
- Secure internal access  

---

## 💡 Solution Implemented

I designed and built a lightweight internal dashboard that:

- Runs locally as a **LAN-hosted server**
- Allows secure login authentication
- Enables multi-level filtering
- Exports search results instantly
- Logs all user activity for audit purposes

The application works within the same Wi-Fi/LAN network:

- My system acts as a local server  
- Other systems on the network can access it via IP  
- No external hosting infrastructure is required  

This created a simple yet effective internal data access system.

---

## 🚀 Key Features

### 🔐 Secure Authentication
- Password hashing using `bcrypt`
- No hardcoded credentials (environment variable based)
- Session timeout (60 minutes)
- Login & logout tracking

### 🔎 Smart Search System
- UHID partial search
- Filter by Hospital Name
- Filter by Speciality
- Combined filtering support

### 📊 Data Processing
- Reads MIS Excel file
- Cleans column names dynamically
- Displays structured tabular output
- Efficient filtering using Pandas

### 📁 Excel Export
- Generates downloadable `search_results.xlsx`
- One-click export functionality

### 📝 Activity Logging
- Login tracking
- Failed login logging
- Search logging
- Logout logging
- Audit trail stored in CSV

---

## 🛠 Tech Stack

- **Python**
- **Gradio**
- **Pandas**
- **Bcrypt**
- **Python-dotenv**
- **Openpyxl**

---

## 📂 Project Structure

```
Healthcare-UHID-Secure-Dashboard/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── .env                # Not uploaded (contains secrets)
├── data/
│   └── MIS_Report.xlsx (Dummy dataset)
├── screenshots/
│   ├── login.png
│   ├── search.png
│   └── results.png
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/Healthcare-UHID-Secure-Dashboard.git
cd Healthcare-UHID-Secure-Dashboard
```

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

---

### 3️⃣ Install Required Libraries

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Create `.env` File

Create a file named `.env` in the root directory:

```
EXCEL_PATH=data/MIS_Report.xlsx

ADMIN_PASSWORD=admin123
SKANDA_PASSWORD=skanda123
SANISH_PASSWORD=sanish123
```

---

## ▶️ How to Run the Application

Run:

```bash
python app.py
```

You will see:

```
Dashboard running at: http://127.0.0.1:7860
LAN access: http://<your-local-ip>:7860
```

---

## 🌐 LAN Access Instructions

To allow other users on the same Wi-Fi network:

1. Ensure all systems are connected to the same network  
2. Share the LAN IP displayed in your terminal  
3. Example:

```
http://192.168.1.25:7860
```

Users can open this link in their browser to access the dashboard.

---

## 🖥 Application Screenshots

### 🔐 Login Page

![Login Page](screenshots/login.png)

---

### 🔎 Search Interface

![Search Page](screenshots/search.png)

---

### 📊 Results & Excel Export

![Results Page](screenshots/results.png)

---

## 📈 Internship Impact

- Reduced repetitive MIS data requests  
- Improved operational turnaround time  
- Enabled self-service reporting  
- Reduced manual Excel workload  
- Improved internal workflow efficiency  
- Demonstrated automation-driven problem solving  

---

## 🔒 Security Considerations

- No real patient data included in repository  
- Environment-based configuration  
- Password hashing using bcrypt  
- Session expiration management  
- Audit logging implemented  

---

## ⚠️ Disclaimer

This repository contains a **dummy dataset version** for demonstration purposes only.  
No confidential healthcare data is included.

---

## 👨‍💻 Author

**Skanda N Raj**  
Software Engineer | Data & Analytics Enthusiast  

---
