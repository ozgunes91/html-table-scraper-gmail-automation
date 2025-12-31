# **n8n Integration — GitHub Workflow Trigger + Artifact Downloader**

This document describes the **n8n automation workflow** that triggers the GitHub Actions pipeline, retrieves the **latest Excel artifact**, and presents it as a **downloadable file** inside n8n.

Your pipeline becomes:

- Fully automated  
- Cloud-executed  
- Download-ready  
- E-mail independent (even if the file is already sent via e-mail, it can also be downloaded directly through n8n)

---

## 🎯 **Purpose**

The n8n workflow:

1. Triggers the GitHub Actions workflow  
2. Waits for it to finish  
3. Fetches the list of workflow artifacts  
4. Selects the **latest** Excel file  
5. Makes it **instantly downloadable** inside n8n  

This allows you to access the scraper output **without entering GitHub or Gmail**.

---

## 🔄 **Workflow Overview**

```
GitHub Workflow Dispatch
    ↓
HTTP Request (dispatch /automation.yml)
    ↓
GitHub: List Artifacts
    ↓
Code Node: Pick Latest Artifact
    ↓
Save Excel Output (Download Artifact)
```

---

## 🧩 **Node-by-Node Explanation**

### **1️⃣ GitHub Workflow Dispatch**
Triggered manually or through Schedule Trigger.

Purpose: Start GitHub Actions run.

---

### **2️⃣ HTTP Request – Dispatch automation.yml**

```
POST https://api.github.com/repos/<user>/<repo>/actions/workflows/automation.yml/dispatches
```

Headers:

```
Authorization: Bearer <PAT>
Accept: application/vnd.github+json
```

---

### **3️⃣ GitHub: List Artifacts**
Fetches all artifacts created by recent workflow runs.

---

### **4️⃣ Code Node — Pick Latest Artifact**

```js
// Extract the JSON payload returned from the previous HTTP Request node
const data = items[0].json;

// GitHub API response structure: { total_count, artifacts: [...] }
const artifacts = data.artifacts || [];

// If no artifacts exist, stop the workflow by returning an empty array
if (artifacts.length === 0) {
	return [];
}

// Sort artifacts by creation date (newest first)
artifacts.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

// Select the most recent artifact
const latest = artifacts[0];

// Return only the latest artifact fields needed for download
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

This ensures **the most recent Excel file** is always selected.

---

## **5️⃣ Save Excel Output (Download Artifact)**

This node:

- Downloads the artifact ZIP  
- Makes it visible in **n8n Execution → Binary**  
- Shows a **Download** button for the user  

📌 *This is the recommended approach — simple and clean.*

---

## ⏱ **Automation / Scheduling**

You may trigger workflow via:

- Daily at a specific time  
- Hourly  
- Every X minutes  
- Manual execution  

Using the **Schedule Trigger** node.

---

## 🌟 **Why This Pipeline Is Professional**

✔ GitHub Actions handles heavy automation  
✔ Python script runs both locally & in cloud  
✔ Excel file never stays on GitHub — securely stored as artifact  
✔ n8n provides UI-based, instant download  
✔ Emails + artifacts = redundancy  
✔ Tam entegrasyon: Python → GitHub Actions → n8n

---

## 🧠 **Architecture Summary**

```
Python Script
    ↓
GitHub Actions (automation.yml)
    ↓
Artifact Upload
    ↓
n8n Workflow
    ↓
Download as Excel
```

Lightweight, secure, scalable.

---

## 👩‍💻 Author

**Özge Güneş**  
Workflow Engineering · Python Automation · CI/CD  
GitHub: https://github.com/ozgunes91  
