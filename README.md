
# **HTML Table Scraper + Excel Export + Gmail Automation**

A fully automated pipeline that **scrapes HTML tables**, **cleans the data**, **exports Excel output**, and **delivers the final file via Gmail** — all powered by Python and enhanced with **GitHub Actions automation**.

This repository demonstrates:

- Web scraping  
- Data cleaning  
- Excel export  
- Secure Gmail automation  
- CI workflow with GitHub Actions  
- Artifact-based file delivery (for n8n integration)

---

## 📁 **Project Structure**

```
html-table-scraper-gmail-automation/
├── html_table_scraper.py        # Main Python scraper script
├── requirements.txt             # Python dependencies
├── README.md                    # Main documentation (this file)
├── .env                         # Email credentials (not committed)
└── .github/
    └── workflows/
        └── automation.yml       # GitHub Actions automation pipeline
```

> `automation.yml` automatically runs the scraper, generates the Excel file, and uploads it as an artifact.

---

## 🚀 **Features**

✔ Scrapes HTML table data  
✔ Parses + cleans + normalizes records  
✔ Saves Excel output  
✔ Sends final file via Gmail  
✔ Credential-safe environment via `.env`  
✔ GitHub Actions triggers script in the cloud  
✔ Artifact output is downloadable by systems like **n8n**

---

## 🔐 **Environment Variables**

Create a `.env` file like this:

```
SCRAPER_SMTP_USER=your_email@gmail.com
SCRAPER_SMTP_PASSWORD=your_gmail_app_password
```
- Gmail requires an App Password (16-character code). Your normal account password will NOT work.
---

## ⚙️ **GitHub Actions (automation.yml)**

Workflow performs:

1. Install Python & dependencies  
2. Run `html_table_scraper.py`  
3. Save the generated Excel file  
4. Upload Excel as **GitHub Artifact**  
5. Allow external automation tools to fetch the artifact  

Triggered via:

- Manual dispatch  
- n8n Webhook / schedule  
- Cron (if enabled)

---
## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/html-table-scraper-automation.git
cd html-table-scraper-automation
```

### 2. Optional: Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# .\venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Script

```bash
python3 html_table_scraper.py
```

Expected output:

```
1) Fetching HTML...
2) Parsing table...
3) Cleaning data...
4) Saving Excel...
Excel saved to: outputs/largest_companies_by_revenue.xlsx
5) Sending email...
📧 Email sent successfully!
🎉 ALL DONE — Automated Pipeline Completed.
```

If SMTP credentials are missing:

```
⚠ SMTP credentials not found in environment. Skipping email sending.
```

---

## 📧 Gmail SMTP Setup

To allow email sending:

✔ Enable 2-Step Verification  
✔ Generate a 16-character App Password  
✔ Put it inside `.env`  

Your actual Gmail password is never used or exposed.

---

## 🔄 Extensions

- Scrape multiple tables  
- Create daily/weekly auto-reports  
- Upload Excel to Google Drive  
- Add KPIs, charts, or analytics  
- Turn the workflow into an automated n8n pipeline  

---
## 🔗 Additional Documentation

Even when the file is successfully delivered via e-mail, the latest Excel output can still be downloaded directly from n8n as well.

📘 n8n Automation Docs → [docs/README_N8N.md](docs/README_N8N.md)

## 👩‍💻 Author

**Özge Güneş**  
Python Automation · Web Scraping · Data Cleaning · Process Automation  
