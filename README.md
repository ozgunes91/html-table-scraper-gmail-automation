# HTML Table Scraper + Excel Export + Gmail Automation

This project demonstrates a complete automation workflow using Python.  
It performs **web scraping**, **data cleaning**, **Excel export**, and **automated email delivery** via Gmail — all while keeping credentials secure using a `.env` file.

---

## 🚀 Overview

This script:

1. Fetches an HTML page from Wikipedia  
2. Extracts the first table on the page  
3. Cleans and normalizes the dataset  
4. Exports the cleaned table into Excel  
5. Sends the Excel file via Gmail automatically  
6. Ensures security using environment variables (no passwords in code)


---

## ✨ Features

- Live web scraping with `requests` + `BeautifulSoup`
- Automatic HTML table extraction using `pandas.read_html`
- MultiIndex → simple snake_case column normalization
- Rank-sorted clean final dataset
- Excel export to `/outputs/`
- Gmail SMTP automation with file attachment
- Secure `.env` variable handling (no exposed passwords)

---

## 📁 Project Structure

```text
html_table_project/
├── html_table_scraper.py   # Main automation script
├── requirements.txt        # Dependency list
├── README.md               # Documentation
├── .gitignore              # Ignores .env and outputs
├── outputs/                # Auto-generated Excel files
└── .env                    # NOT uploaded to GitHub (credentials)
```

---

## 🔐 Environment Variables

Create a `.env` file in the project directory:

```env
SCRAPER_SMTP_USER=your_gmail_address@gmail.com
SCRAPER_SMTP_PASSWORD=your_16_character_gmail_app_password
```

These variables are loaded automatically:

```python
from dotenv import load_dotenv
load_dotenv()
```

### ⚠ Security Notes

- `.env` is ignored via `.gitignore`  
- Credentials are never visible in code or commits  
- Safe for public repositories  
- App passwords are required (not your real Gmail password)

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

## 👩‍💻 Author

**Özge Güneş**  
Python Automation · Web Scraping · Data Cleaning · Process Automation  

