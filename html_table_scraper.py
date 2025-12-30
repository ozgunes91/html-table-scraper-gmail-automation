"""
HTML Table Scraper + Gmail Automation
Author: Özge Güneş
Description:
    Fetches, parses, cleans and exports a business table from Wikipedia,
    then automatically emails the generated Excel file using Gmail SMTP.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from typing import Optional
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"
load_dotenv(env_path)

# ---------------------------------------------------------
# 1) Fetch HTML
# ---------------------------------------------------------
def fetch_html(url: str) -> str:
    """Fetch HTML content from the given URL using a safe User-Agent."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; OzgeScraper/1.0)"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text


# ---------------------------------------------------------
# 2) Parse table using BS4 + Pandas
# ---------------------------------------------------------
def parse_table(html: str) -> pd.DataFrame:
    """Extract the first HTML table and convert it into a DataFrame."""
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")

    if table is None:
        raise ValueError("No table found on the page.")

    dfs = pd.read_html(StringIO(str(table)))
    return dfs[0]


# ---------------------------------------------------------
# 3) Clean DataFrame
# ---------------------------------------------------------
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize the extracted DataFrame.

    - Flatten MultiIndex columns, if present
    - Normalize raw column names
    - Rename to readable, business-friendly names
    - Drop useless columns
    - Clean text fields
    - Convert numeric columns to proper numeric types
    """
    cleaned = df.copy()

    # 0) If columns are MultiIndex, flatten them first
    if isinstance(cleaned.columns, pd.MultiIndex):
        flat_cols = []
        for col_tuple in cleaned.columns:
            # remove None / nan parts and join non-empty pieces with space
            parts = [str(part).strip() for part in col_tuple if part and str(part) != "nan"]
            name = " ".join(parts)
            flat_cols.append(name if name else "column")
        cleaned.columns = flat_cols
    else:
        cleaned.columns = list(cleaned.columns)

    # 1) Normalize column names (lowercase, underscores, remove weird chars)
    cleaned.columns = (
        pd.Index(cleaned.columns)
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^\w_]", "", regex=True)
        .str.lower()
    )

    # 2) Rename ugly columns to nice business names
    rename_map = {
        "ranks_ranks": "rank",
        "ranks": "rank",
        "name_name": "company",
        "name": "company",
        "industry_industry": "industry",
        "industry": "industry",
        "revenue_usd_in_millions": "revenue_usd_million",
        "revenue_musd": "revenue_usd_million",
        "profit_usd_in_millions": "profit_usd_million",
        "employees_employees": "employees",
        "employees": "employees",
        "headquartersnote_1_headquartersnote_1": "headquarters",
        "headquartersnote_1": "headquarters",
        "stateowned_stateowned": "state_owned",
        "state_owned": "state_owned",
        "ref_ref": "reference",
        "ref": "reference",
    }
    cleaned = cleaned.rename(columns={k: v for k, v in rename_map.items() if k in cleaned.columns})

    # 3) Drop useless "unnamed" columns
    drop_cols = [c for c in cleaned.columns if "unnamed" in c]
    if drop_cols:
        cleaned = cleaned.drop(columns=drop_cols, errors="ignore")

    # 4) Clean text columns (strip newlines, extra spaces)
    text_cols = ["company", "industry", "headquarters", "reference"]
    for col in text_cols:
        if col in cleaned.columns:
            cleaned[col] = (
                cleaned[col]
                .astype(str)
                .str.replace(r"\s+", " ", regex=True)
                .str.strip()
            )

    # 5) Convert numeric columns
    numeric_cols = ["revenue_usd_million", "profit_usd_million", "employees"]
    for col in numeric_cols:
        if col in cleaned.columns:
            cleaned[col] = (
                cleaned[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("$", "", regex=False)
                .str.replace(" ", "", regex=False)
                .str.replace(r"\[[^\]]*\]", "", regex=True)
            )
            cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    # 6) Clean reference column (remove [ ] if still there)
    if "reference" in cleaned.columns:
        cleaned["reference"] = (
            cleaned["reference"]
            .astype(str)
            .str.replace(r"[\[\]]", "", regex=True)
            .str.strip()
        )

    # 7) Drop fully empty rows
    cleaned = cleaned.dropna(how="all").reset_index(drop=True)

    # 8) Remove state-owned column (no longer provided by Wikipedia)
    if "state_owned" in cleaned.columns:
        cleaned.drop(columns=["state_owned"], inplace=True)

    # 9) Remove reference column (not needed in final business report)
    if "reference" in cleaned.columns:
        cleaned.drop(columns=["reference"], inplace=True)

    # 10) Sort rows by rank (original business order)
    if "rank" in cleaned.columns:
        cleaned = cleaned.sort_values("rank").reset_index(drop=True)

    return cleaned

# ---------------------------------------------------------
# 4) Save Excel
# ---------------------------------------------------------
def save_excel(df: pd.DataFrame, filename: str) -> Path:
    """Save DataFrame as Excel and return file path."""
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    file_path = output_dir / filename
    df.to_excel(file_path, index=False)
    return file_path


# ---------------------------------------------------------
# 5) Email the file via Gmail (credentials from environment)
# ---------------------------------------------------------

def send_email(file_path: Path, receiver_email: Optional[str] = None):
    """
    Send an email with the Excel file attached using Gmail SMTP.

    Credentials are read from environment variables:
        SCRAPER_SMTP_USER      -> Gmail address
        SCRAPER_SMTP_PASSWORD  -> 16-character Gmail app password
    """
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    sender_email = os.getenv("SCRAPER_SMTP_USER")
    smtp_password = os.getenv("SCRAPER_SMTP_PASSWORD")

    if not sender_email or not smtp_password:
        print("⚠ SMTP credentials not found in environment. Skipping email sending.")
        return

    if receiver_email is None:
        receiver_email = sender_email  # send the report to yourself by default

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Your Scraped Data File (Automated by Özge's Script)"

    body = "Hi! Your automated data scraping task has completed.\nExcel file is attached."
    msg.attach(MIMEText(body, "plain"))

    # Attach file
    with open(file_path, "rb") as f:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(f.read())

    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", f"attachment; filename={file_path.name}")
    msg.attach(attachment)

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, smtp_password)
        server.send_message(msg)

    print("📧 Email sent successfully!")


# ---------------------------------------------------------
# MAIN WORKFLOW
# ---------------------------------------------------------
def main():
    url = "https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue"

    print("1) Fetching HTML...")
    html = fetch_html(url)

    print("2) Parsing table...")
    df_raw = parse_table(html)

    print("3) Cleaning data...")
    df_clean = clean_dataframe(df_raw)

    print("4) Saving Excel...")
    file_path = save_excel(df_clean, "largest_companies_by_revenue.xlsx")
    print(f"Excel saved to: {file_path}")

    print("5) Sending email...")
    # By default, send to the same address as SCRAPER_SMTP_USER
    # If you want to use a different recipient, you can read another env var here.
    send_email(file_path)

    print("🎉 ALL DONE — Automated Pipeline Completed.")


if __name__ == "__main__":
    main()
