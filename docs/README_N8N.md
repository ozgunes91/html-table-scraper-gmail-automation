<div align="center">

# 🔁 **n8n Workflow — GitHub Trigger + Excel Artifact Downloader**
### Cloud Automation · CI/CD Orchestration · GitHub API Integration

![n8n](https://img.shields.io/badge/n8n-Automation-orange?style=for-the-badge)
![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-Scraper-yellow?style=for-the-badge)

</div>

---

# 🎯 Purpose

This workflow allows n8n to:

1. Trigger GitHub Actions  
2. Wait for the Python script to execute  
3. Fetch the latest Excel artifact  
4. Provide the artifact directly as a downloadable file  

---

# 🔧 Node‑by‑Node Breakdown

## **1️⃣ Schedule / Manual Trigger (Start Node)**  
Starts the pipeline either at a set time (cron) or manually.

---

## **2️⃣ HTTP Request — Trigger GitHub Actions**

```http
POST https://api.github.com/repos/<user>/<repo>/actions/workflows/automation.yml/dispatches
Authorization: Bearer <GitHub PAT>
Accept: application/vnd.github+json
```

This invokes the `workflow_dispatch` event.

---

## **3️⃣ GitHub API — List Artifacts**

Fetches all workflow artifacts.  
Returns JSON:

```json
{
  "total_count": ...,
  "artifacts": [...]
}
```

---

## **4️⃣ Code Node — Pick Latest Artifact**

```javascript
const data = items[0].json;
const artifacts = data.artifacts || [];

if (!artifacts.length) return [];

artifacts.sort((a, b) =>
  new Date(b.created_at) - new Date(a.created_at)
);

const latest = artifacts[0];

return [
  {
    json: {
      artifact_id: latest.id,
      artifact_name: latest.name,
      download_url: latest.archive_download_url,
      created_at: latest.created_at
    }
  }
];
```

Always selects the most recent Excel build.

---

## **5️⃣ Download Artifact (Binary File Node)**

- Downloads the ZIP containing the Excel file  
- Makes it available inside n8n UI  
- Allows one‑click download  

---

# 📌 Key Clarifications

### ✔ n8n **does not send email**  
The email is always sent by the Python script (locally or in GitHub Actions).

### ✔ GitHub Actions runs the scraper  
n8n only triggers it and retrieves the output.

### ✔ n8n can run autonomously  
Thanks to the schedule node.

---

# 🧠 Full Automation View

```text
n8n trigger
    ↓
HTTP → workflow_dispatch
    ↓
GitHub Actions
    ↓
Python:
 scrape → clean → Excel → email → artifact
    ↓
Artifact Storage
    ↓
n8n:
 fetch → pick latest → download
```

---

<div align="center">

### ⚡ *Automation engineered with precision by **Özge Güneş***  

</div>
