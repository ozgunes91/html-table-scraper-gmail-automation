<div align="center">

# 🚀 **HTML Table Scraper → Excel Generator → Email Automation**
### **Python · GitHub Actions · n8n · CI/CD · Automated Reporting Pipeline**

![Status](https://img.shields.io/badge/Status-Production_GRADE-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge)
![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-black?style=for-the-badge)
![n8n](https://img.shields.io/badge/n8n-Automation-orange?style=for-the-badge)
![Excel](https://img.shields.io/badge/Excel-Reports-success?style=for-the-badge)

</div>

---

# 📌 Project Overview

This project performs **end‑to‑end automated web data extraction**, **data cleaning**, **Excel generation**, and **email delivery**, with optional **GitHub Actions CI/CD** and **n8n orchestration**.

It demonstrates a multi‑environment automation architecture:

### ✔ Local Python execution  
### ✔ GitHub Actions cloud execution  
### ✔ n8n workflow orchestration (manual or scheduled)

---

# 🧠 Architecture Overview

## **1 — Data Processing Pipeline**

```text
Wikipedia Page
     ↓
Python Script
(scrape → clean → Excel → email)
     ↓
Excel Output (.xlsx)
     ↓
Email Delivery (if SMTP configured)
```

---

## **2 — Complete Orchestration Pipeline (n8n → GitHub → Python → n8n)**

```text
n8n Trigger (Cron or Manual)
     ↓
HTTP Request → GitHub Actions (workflow_dispatch)
     ↓
GitHub Actions
  - Install dependencies
  - Run Python script in cloud
  - Upload Excel as artifact
  - Email sent by Python script
     ↓
Artifact Storage (GitHub)
     ↓
n8n
  - List artifacts
  - Pick latest
  - Download binary (Excel)
```

This is the **real execution order**, matching actual behavior exactly.

---

# 🐍 Python Script — Full Feature Breakdown

The Python script (`html_table_scraper.py`) performs 5 fully automated steps:

---

## **1️⃣ Download HTML Page**
- Uses `requests` with custom headers  
- Fetches a Wikipedia table page  
- Includes timeout & error handling  

---

## **2️⃣ Parse First HTML Table**
- `BeautifulSoup` selects the table  
- `pandas.read_html()` converts it to a DataFrame  
- Handles multi‑index columns  

---

## **3️⃣ Data Cleaning**
✔ Flattens multi‑index column headers  
✔ Normalizes column names  
✔ Renames technical columns:  
- `revenue_usd_in_millions` → `revenue_usd_million`  
- `employees_employees` → `employees`  
- `headquartersnote_1` → `headquarters`

✔ Removes:  
- unnamed columns  
- empty rows  
- irrelevant metadata columns (state-owned, reference)  

✔ Automatically sorts by `rank`

This results in a clean, analysis‑ready dataset.

---

## **4️⃣ Save Excel Output**

Excel is exported to:

```
outputs/largest_companies_by_revenue.xlsx
```

---

## **5️⃣ Email Delivery (SMTP Gmail)**

If `.env` contains valid Gmail App Password credentials:

- The script generates an email  
- Attaches the Excel file  
- Sends it via Gmail SMTP  

👉 If SMTP not configured, the script skips email gracefully.

---

# 🟦 GitHub Actions Workflow

File: `.github/workflows/automation.yml`

GitHub Actions provides:

✔ Cloud execution  
✔ Dependency isolation  
✔ Reproducibility  
✔ Secure secrets management  
✔ Artifact generation  

Steps:

1. Setup Python  
2. Install requirements  
3. Run the scraper script  
4. Email is sent by Python  
5. Excel is uploaded as a GitHub Artifact  

This allows fully cloud‑based automation without local execution.

---

# 🔁 n8n Integration (High‑Level Summary)

n8n provides:

- **Manual execution**
- **Scheduled execution (cron)**
- **Triggering GitHub Actions via HTTP**
- **Downloading the latest artifact**
- **UI‑based binary download**

n8n **does not send email** in this project;  
email is always handled by the Python script.

---

# 📁 Project Structure

```
html-table-scraper-gmail-automation/
│
├── html_table_scraper.py
├── requirements.txt
├── README.md
│
├── outputs/
│   └── largest_companies_by_revenue.xlsx
│
├── .github/
│   └── workflows/
│       └── automation.yml
│
└── docs/
    ├── README_N8N.md
    ├── html-table-scraper-gmail-automation.json
    └── automation.png
```

---

# ▶️ How to Run Locally

### 1. Install requirements
```
pip install -r requirements.txt
```

### 2. Add `.env` file
```
SCRAPER_SMTP_USER=your_email@gmail.com
SCRAPER_SMTP_PASSWORD=your_app_password
```

### 3. Run the script
```
python html_table_scraper.py
```

---

# 🧩 Execution Options Summary

| Method | Sends Email | Generates Excel | Stores Artifact | Requires Setup |
|--------|-------------|-----------------|-----------------|----------------|
| Local Python | ✅ | ✅ | ❌ | `.env` for SMTP |
| GitHub Actions | ✅ | ✅ | ✅ | GitHub Secrets |
| n8n | (via Python) | (via Python) | Download available | GitHub token |

---

# 👩‍💻 Author  
**Özge Güneş**  
Automation • Python • Workflow Engineering  

<div align="center">

### ⭐ *If this project helps you, consider starring the repository!*

</div>
