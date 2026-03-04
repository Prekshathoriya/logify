# 📋 Logify – Smart Daily Work Logging System

Logify is a simple, personal EOD (End of Day) logging tool built with **Streamlit** and **Google Sheets**.

Every day you write what you worked on, hit Save, and your entry is stored permanently in a Google Sheet — forever, for free. No database setup, no backend, no complexity.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📅 Auto Date & Day | No typing needed — date and day are filled automatically |
| 🔒 One Entry Per Day | Duplicate entries are blocked automatically |
| 🔥 Streak Tracker | See how many consecutive days you've logged |
| 📊 Monthly Counter | Track how many days you logged this month |
| ✨ Polish My EOD | Improves your text to sound more professional |
| 📥 Export to Excel | Download all your logs as a .xlsx file |

---

## 🗂️ Project Structure

```
logify/
├── app.py                 ← Main Streamlit app (all logic lives here)
├── requirements.txt       ← Python packages needed
├── README.md              ← This file
└── service_account.json   ← Your Google API credentials (DO NOT share this)
```

---

## 🚀 Setup Guide (Step by Step)

### Step 1 – Install Python packages

Make sure you have Python 3.9+ installed. Then run:

```bash
pip install -r requirements.txt
```

---

### Step 2 – Set up Google Sheets API

This is the most important step. Follow carefully.

#### 2a. Create a Google Cloud Project

1. Go to [https://console.cloud.google.com](https://console.cloud.google.com)
2. Click **"New Project"** → give it any name (e.g. `logify-project`) → Click **Create**
3. Make sure your new project is selected in the top dropdown

#### 2b. Enable the APIs

1. In the left sidebar, go to **APIs & Services → Library**
2. Search for **"Google Sheets API"** → Click it → Click **Enable**
3. Go back to Library, search for **"Google Drive API"** → Click it → Click **Enable**

#### 2c. Create a Service Account

> A service account is like a robot Google account that your app uses to read/write the sheet.

1. Go to **APIs & Services → Credentials**
2. Click **"+ Create Credentials"** → Choose **"Service Account"**
3. Give it a name like `logify-bot` → Click **Create and Continue**
4. Skip the optional steps → Click **Done**

#### 2d. Download the JSON Key

1. Click on the service account you just created
2. Go to the **"Keys"** tab
3. Click **"Add Key"** → **"Create New Key"** → Choose **JSON** → Click **Create**
4. A file will download automatically — this is your `service_account.json`
5. **Move this file into your `logify/` project folder**

> ⚠️ NEVER share this file or upload it to GitHub. Add it to `.gitignore`.

#### 2e. Share your Google Sheet with the service account

1. Open `service_account.json` in a text editor
2. Find the `"client_email"` field — it looks like: `logify-bot@your-project.iam.gserviceaccount.com`
3. Go to [Google Sheets](https://sheets.google.com) and create a new blank sheet named exactly:
   ```
   Logify - Work Logs
   ```
4. Click **Share** (top right) → paste the `client_email` → give it **Editor** access → Click **Send**

> 💡 Alternatively, the app will auto-create the sheet the first time it runs — but sharing manually ensures no permission issues.

---

### Step 3 – Run Locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## ☁️ Deploy on Streamlit Community Cloud (Free)

Streamlit Cloud lets you host your app for free at a public URL.

### Step 1 – Push your code to GitHub

Create a new GitHub repository. Push your project files:

```
app.py
requirements.txt
README.md
```

> ⚠️ DO NOT push `service_account.json` to GitHub. Add it to `.gitignore`.

### Step 2 – Add secrets on Streamlit Cloud

Since you can't upload `service_account.json` to GitHub, you'll store the credentials as **Streamlit Secrets**.

1. Go to [https://share.streamlit.io](https://share.streamlit.io) and log in with GitHub
2. Click **"New App"** → select your repo and branch → set main file to `app.py`
3. Before deploying, click **"Advanced settings"** → go to the **Secrets** tab
4. Open your `service_account.json` file and paste its contents in this format:

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "abc123..."
private_key = "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"
client_email = "logify-bot@your-project.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

> 💡 Copy each field from `service_account.json` and paste them here in TOML format.

5. Click **Deploy** — your app will be live in ~1 minute!

---

## 🧠 How Key Features Work

### 🔥 Streak Logic

The streak counter walks backwards through dates:

```
Today = March 4
Check March 4 → has entry? ✅ streak = 1
Check March 3 → has entry? ✅ streak = 2
Check March 2 → has entry? ✅ streak = 3
Check March 1 → has entry? ❌ STOP
→ Final streak = 3
```

If you miss a day, the streak resets to 0 (or whatever your current consecutive run is).

### 🔌 Google Sheets Connection

```
Your App → service_account.json credentials
         → Google authenticates the service account
         → App gets read/write access to your sheet
         → gspread library handles all the API calls
```

No passwords, no OAuth popups — it all happens in the background automatically.

---

## 🛑 .gitignore (Important!)

Create a `.gitignore` file in your project folder with this content:

```
service_account.json
__pycache__/
*.pyc
.env
```

This prevents your secret credentials from being accidentally pushed to GitHub.

---

## 📄 License

Free to use for personal and portfolio projects.
