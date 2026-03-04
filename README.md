# Logify - Smart Daily Work Logging System

Logify is a simple, multi-user EOD (End of Day) logging tool built with Streamlit and Google Sheets.

Every day you enter your name, write what you worked on, and hit Save. Your entry is stored permanently in a Google Sheet. Each user sees only their own logs, streak, and stats.

Live App: https://logify-rd2yvxupcn4ykvwb8wsgjk.streamlit.app
GitHub: https://github.com/Prekshathoriya/logify

---

## Features

- Multi-user support - each person enters their name and gets their own private view
- Auto date and day detection - no typing needed
- One entry per day - duplicate entries are blocked automatically
- Streak tracker - counts how many consecutive days you have logged
- Monthly counter - tracks how many days you logged this month
- Polish My EOD - improves your text to sound more professional
- Export to Excel - download all your logs as a .xlsx file
- IST timezone - all times are recorded in Indian Standard Time

---

## Project Structure

```
logify/
├── app.py                 - Main Streamlit app
├── requirements.txt       - Python packages needed
├── README.md              - This file
└── service_account.json   - Google API credentials (DO NOT share or upload to GitHub)
```

---

## How Multi-User Works

All users' logs are stored in one single Google Sheet called "Logify - Work Logs".

Each row has a Name column:

| Name    | Date        | Day      | Work Done Today | Submission Time |
|---------|-------------|----------|-----------------|-----------------|
| Preksha | 05 Mar 2026 | Thursday | Completed...    | 06:30 PM        |
| Mentor  | 05 Mar 2026 | Thursday | Reviewed...     | 07:00 PM        |
| John    | 05 Mar 2026 | Thursday | Fixed bug...    | 08:00 PM        |

When a user opens the app and enters their name, they only see their own rows. The streak, stats, and export are all filtered per user.

The sheet owner (you) can open the Google Sheet and see everyone's entries in one place - great for mentors tracking their students.

---

## Setup Guide

### Step 1 - Install Python packages

```bash
pip install -r requirements.txt
```

### Step 2 - Set up Google Sheets API

#### 2a. Create a Google Cloud Project
1. Go to https://console.cloud.google.com
2. Click New Project, give it a name, click Create

#### 2b. Enable APIs
1. Go to APIs and Services - Library
2. Search and enable Google Sheets API
3. Search and enable Google Drive API

#### 2c. Create a Service Account
1. Go to APIs and Services - Credentials
2. Click Create Credentials - Service Account
3. Give it a name like logify-bot - click Create and Continue
4. Skip optional steps - click Done

#### 2d. Download the JSON Key
1. Click on your service account
2. Go to the Keys tab
3. Click Add Key - Create New Key - JSON - Create
4. Rename the downloaded file to service_account.json
5. Move it into your logify folder

#### 2e. Create and Share the Google Sheet
1. Go to https://sheets.google.com
2. Create a new blank sheet
3. Rename it to exactly: Logify - Work Logs
4. Click Share - paste your service account email - set role to Editor - click Share

### Step 3 - Run Locally

```bash
streamlit run app.py
```

App opens at http://localhost:8501

---

## Deploy on Streamlit Cloud (Free)

### Step 1 - Push to GitHub
Push your project to a GitHub repository. Do NOT include service_account.json in the repo.

### Step 2 - Add Secrets on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click New App - select your repo - set main file to app.py
3. Click Advanced Settings - Secrets tab
4. Paste your credentials in TOML format:

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-client-x509-cert-url"
universe_domain = "googleapis.com"
```

### Step 3 - Deploy
Click Deploy. Your app will be live in about 2 minutes.

---

## Important Notes

- Never upload service_account.json to GitHub
- The .gitignore file already excludes it
- All times are recorded in IST (Indian Standard Time)
- The Google Sheet must be named exactly: Logify - Work Logs
- The service account email must have Editor access to the sheet

---

## Tech Stack

- Frontend: Streamlit
- Database: Google Sheets
- Language: Python
- Deployment: Streamlit Community Cloud (free)
- Libraries: gspread, google-auth, pandas, openpyxl

---

## Built By

Preksha Thoriya
GitHub: https://github.com/Prekshathoriya
Project: https://github.com/Prekshathoriya/logify
