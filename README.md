# HTML Table Scraper → Excel Generator → Email Automation  
*A small, end-to-end automation pipeline built with Python, GitHub Actions and n8n.*

---

## 🧩 Project Story

This project was created to automatically extract an HTML table from the web, clean it, convert it into a polished Excel file, and make it easily deliverable through different automation channels.

The goal is simple:

**“Fetch data → Clean it → Convert to Excel → Deliver it — with one click or fully automated.”**

The pipeline demonstrates a modular structure that can adapt to multiple execution styles depending on user needs.

---

## ⚙️ Core Methodology

This automation consists of three independent but compatible components:

1. **Python script**  
   - Scrapes an HTML table  
   - Cleans and normalizes the data  
   - Converts it into Excel  
   - Sends the Excel via Gmail (if credentials are configured)

2. **GitHub Actions workflow**  
   - Executes the same Python script in a clean cloud environment  
   - Publishes the resulting Excel as an Artifact  
   - Can be triggered manually from the Actions tab

3. **n8n workflow**  
   - Can trigger the GitHub Actions workflow  
   - Downloads the latest Excel artifact  
   - Makes the Excel file downloadable inside n8n  
   - Optionally emails the file again  
   - Can run on a schedule (e.g., daily delivery)

This gives flexibility for different user types:
- Developers → use GitHub Actions  
- Non-technical users → use n8n  
- Local testing → run Python script directly

---

# 🧠 Architecture Overview

```
Wikipedia Page
        │
        ▼
  Python Script
  (scrape → parse → clean → Excel → email)
        │
        │  (optional: triggered in the cloud)
        ▼
 GitHub Actions Workflow
  - Runs python script
  - Publishes Excel as Artifact
        │
        ▼
        n8n
  - Triggers workflow (manual or scheduled)
  - Fetches latest Artifact
  - Downloads Excel
  - Sends email (optional)
  - Exposes Excel as downloadable output
```

This architecture matches **exactly** how the project works in reality.

---

# 🐍 1. Python Script (Real Functional Steps)

File: `html_table_scraper.py`  
A fully functional pipeline consisting of 5 real stages:

### ✔ 1. Fetch HTML  
- Uses `requests`  
- Custom User-Agent + timeout for reliability  
- Downloads raw HTML from the Wikipedia page

### ✔ 2. Parse first HTML `<table>`  
- `BeautifulSoup` locates the table  
- `pandas.read_html` parses it into a DataFrame

### ✔ 3. Clean the DataFrame  
The script performs **real cleaning logic**:

- Flattens MultiIndex columns  
- Normalizes column names  
- Renames messy technical names to human-friendly ones  
  - `revenue_usd_in_millions` → `revenue_usd_million`  
  - `employees_employees` → `employees`  
  - `headquartersnote_1` → `headquarters`
- Removes “unnamed” columns  
- Drops blank rows  
- Removes optional columns (`state_owned`, `reference`) if present  
- Sorts by `rank` column when available  

### ✔ 4. Save Excel  
Saves the cleaned DataFrame automatically to:

```
outputs/largest_companies_by_revenue.xlsx
```

### ✔ 5. Gmail Email Send  
- Uses `smtp.gmail.com:587`  
- Loads credentials from `.env`  
- If credentials missing → prints warning and skips email  
- Otherwise → sends the Excel file as an email attachment

The script alone provides a complete “scrape → clean → Excel → email” pipeline.

---

# 🟦 2. GitHub Actions Workflow (automation.yml)

The repository includes:

```
.github/workflows/automation.yml
```

This workflow:

- Installs Python + dependencies  
- Runs the same Python script in the cloud  
- Generates the Excel file  
- Publishes it as a **GitHub Artifact**  
- Is triggered manually via **Run workflow**  
- Does **not** include cron (optional)

This makes the pipeline reproducible and cloud-ready.

---

# 🟩 3. n8n Workflow

Stored under `docs/html-table-scraper-gmail-automation.json`.

The real n8n workflow performs:

1. Triggers the GitHub Actions workflow (workflow_dispatch)  
2. Retrieves the list of artifacts from the GitHub API  
3. Selects the **latest artifact** via a Code node  
4. Downloads the Excel artifact  
5. Optionally emails it via Gmail node  
6. Makes the file downloadable inside n8n  
7. Supports scheduled runs (Cron)

This provides a no-code UI for automated report delivery.

---

# 🔧 Execution Options (Flexible by Design)

This pipeline intentionally supports **three execution styles**:

### **1) Local Python run**
```bash
python html_table_scraper.py
```
Scrapes → cleans → exports → emails.

### **2) GitHub Actions (manual trigger)**
From the Actions tab:
- Click **Run workflow**  
- The workflow runs the script in CI and uploads the Excel as an artifact.

### **3) n8n workflow**
- Can run on a schedule (daily)  
- Can run manually (single click)  
- Automatically fetches the latest Excel artifact  
- Can email the Excel again  
- Allows direct downloading in the n8n UI

All three methods produce the **same Excel output**.

---

# 📁 Project Structure

```
html-table-scraper-gmail-automation/
│
├── html_table_scraper.py               # scrape → clean → Excel → email
├── requirements.txt                    # Python dependencies
├── README.md                           # Main documentation
│
├── outputs/
│   └── largest_companies_by_revenue.xlsx   # Real Excel output
│
├── .env (not committed)                # Local SMTP credentials
│
├── .github/
│   └── workflows/
│       └── automation.yml              # GitHub Actions workflow
│
└── docs/
    ├── README_N8N.md
    ├── html-table-scraper-gmail-automation.json
    └── automation.png
```

---

# ▶️ Local Usage

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add `.env`
```env
SCRAPER_SMTP_USER=your_email@gmail.com
SCRAPER_SMTP_PASSWORD=your_app_password
```

### 3. Run script
```bash
python html_table_scraper.py
```

Produces:

- Excel under `outputs/`  
- Email (if SMTP configured)

---

# 🐾 Notes

- Do **not** commit your `.env`  
- Gmail requires an **App Password**  
- n8n always retrieves the latest artifact  
- GitHub Actions run is manual, but scheduling can be added if needed

---

# 👩‍💻 Author

**Özge Güneş**  
Automation • Python • Web Scraping • Data Cleaning • Workflow Design
