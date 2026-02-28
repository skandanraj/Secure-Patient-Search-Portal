# 🏥 Healthcare UHID Secure Dashboard  

---

## 📌 Project Overview

During my internship at **Aster DM Healthcare**, the operational team frequently reached out to the MIS team for patient appointment details, UHID-based records, hospital-specific data, and payment information.

This repetitive manual process caused:

- Delays in operations  
- Increased dependency on the MIS team  
- Repeated data extraction tasks  

To solve this problem, I designed and developed an internal **UHID Search Dashboard** using **Python and Gradio**, allowing the operations team to independently search and download required patient records over the internal LAN network.

---

## 🎯 Problem Statement

The operational team required:

- Quick access to patient appointment details  
- Hospital and speciality-based filtering  
- Payment and invoice tracking  
- Exportable data for reporting  
- Reduced dependency on the MIS team  

Before this solution:

- Every request required manual Excel filtering  
- MIS team handled repetitive data extraction  
- Operational efficiency was impacted  

---

## 💡 Solution Implemented

I built a secure web-based dashboard that:

- Runs locally as a **LAN-hosted internal server**
- Allows authorized users to log in securely
- Enables multi-level data filtering
- Exports search results instantly to Excel
- Maintains activity logs for audit tracking

The application works on the **same Wi-Fi/LAN network**, where:

- My system acts as the local server  
- Other systems within the network can access the dashboard  
- No external hosting infrastructure is required  

---

## 🚀 Key Features

### 🔐 Secure Authentication
- Password hashing using **bcrypt**
- No hardcoded credentials (environment variable based)
- Session timeout (60 minutes)
- Login & logout tracking

### 🔎 Advanced Search Capabilities
- Search by UHID (partial match supported)
- Filter by Hospital Name
- Filter by Speciality
- Combined filter functionality

### 📊 Data Handling
- Reads from MIS Excel file
- Dynamic column cleaning
- Structured result display
- Efficient filtering using Pandas

### 📁 Excel Export
- Download filtered results instantly
- Automated export file generation (`search_results.xlsx`)

### 📝 Activity Logging
- Login tracking
- Failed login tracking
- Search history logging
- Logout logging
- Audit trail maintenance

---

## 🛠 Tech Stack

- **Python**
- **Gradio** (UI Framework)
- **Pandas** (Data Processing)
- **Bcrypt** (Password Security)
- **Python-dotenv** (Secure Configuration)
- **Openpyxl** (Excel Operations)

---

## 🌐 Deployment Architecture

- Hosted locally using:
  
  ```python
  app.launch(server_name="0.0.0.0", server_port=7860)
