# Setup Guide - Using Streamlit Secrets

## 🔐 Using Streamlit Secrets (Recommended)

Streamlit secrets are more secure than hardcoding credentials and work seamlessly in both local development and cloud deployment.

## Quick Setup

### Step 1: Create Secrets File (Local Development)

```bash
# Create .streamlit directory
mkdir .streamlit

# Create secrets.toml file
touch .streamlit/secrets.toml
```

### Step 2: Add Your Credentials

Edit `.streamlit/secrets.toml` and add:

```toml
# Firebase Configuration
[firebase]
apiKey = "AIzaSy..."
authDomain = "your-project.firebaseapp.com"
projectId = "your-project"
storageBucket = "your-project.appspot.com"
messagingSenderId = "123456789"
appId = "1:123:web:abc123"
databaseURL = "https://your-project-default-rtdb.firebaseio.com"

# Firebase Service Account
[firebase.serviceAccount]
type = "service_account"
project_id = "your-project"
private_key_id = "abc123..."
private_key = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
-----END PRIVATE KEY-----"""
client_email = "firebase-adminsdk-...@your-project.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."

# OpenAI API Key
[openai]
api_key = "sk-..."
```

**Important Notes:**
- Use triple quotes `"""` for the private_key (it's multiline)
- Keep the `-----BEGIN/END PRIVATE KEY-----` lines
- Don't commit this file to Git!

### Step 3: Add to .gitignore

```bash
echo ".streamlit/secrets.toml" >> .gitignore
```

### Step 4: Get Your Firebase Credentials

1. **Go to Firebase Console:** https://console.firebase.google.com/
2. **Select your project** (or create new one)

**Get Web App Config:**
3. Project Settings > General > Your apps
4. Click web icon `</>` or select existing web app
5. Copy the `firebaseConfig` object values

**Get Service Account:**
6. Project Settings > Service Accounts
7. Click "Generate new private key"
8. Download the JSON file
9. Copy the values into your secrets.toml

**Enable Services:**
10. Authentication > Sign-in method > Enable "Email/Password"
11. Realtime Database > Create database > Start in test mode

### Step 5: Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy to secrets.toml under `[openai]`

### Step 6: Test Locally

```bash
streamlit run app_simplified.py
```

You should see:
- ✅ Login page appears
- ✅ No credential errors
- ✅ Can create account

---

## 🚀 Deploying to Streamlit Cloud

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/java-learning-study.git
git push -u origin main
```

**Make sure `.streamlit/secrets.toml` is in .gitignore!**

### Step 2: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Connect your GitHub repository
4. Select branch: `main`
5. Main file: `app_research.py`
6. Click "Deploy"

### Step 3: Add Secrets in Streamlit Cloud

1. After deployment, go to **App Settings** (three dots menu)
2. Click **Secrets**
3. Copy your ENTIRE `.streamlit/secrets.toml` content
4. Paste into the secrets editor
5. Click **Save**

Your app will automatically restart with the secrets loaded!

---

## 📁 Project Structure

```
your-project/
├── app_research.py          # Main app
├── config.py                # Study settings
├── firebase_config.py       # Loads from secrets
├── auth.py                  # Authentication
├── database.py              # Data operations
├── research_topics.py       # Content
├── static_quiz.py           # Quizzes
├── survey.py                # Surveys
├── data_export.py           # CSV export
├── ai_client.py             # OpenAI client
├── characters.py            # Character personalities
├── tutor_flow.py            # Scaffolding logic
├── visuals.py               # Diagrams
├── .gitignore               # Ignore secrets!
├── .streamlit/
│   ├── secrets.toml         # YOUR CREDENTIALS (not in Git)
│   └── secrets.toml.example # Template
└── requirements.txt         # Dependencies
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Use `.streamlit/secrets.toml` for all credentials
- Add secrets.toml to .gitignore
- Use secrets.toml.example as template (safe to commit)
- Rotate keys if accidentally exposed
- Use Streamlit Cloud's secrets manager

### ❌ DON'T:
- Hardcode credentials in Python files
- Commit secrets.toml to Git
- Share secrets.toml file
- Post secrets in issues/forums
- Use the same Firebase project for dev & prod

---

## 🧪 Testing Your Setup

### Test 1: Secrets Loading

```python
import streamlit as st

# Test if secrets are accessible
try:
    firebase_key = st.secrets["firebase"]["apiKey"]
    openai_key = st.secrets["openai"]["api_key"]
    print("✅ Secrets loaded successfully!")
except Exception as e:
    print(f"❌ Error loading secrets: {e}")
```

### Test 2: Firebase Connection

Run the app and try to:
1. Create an account
2. Login
3. Check Firebase console to see user

### Test 3: OpenAI Connection

Start a session and:
1. Type a message
2. Should get AI response
3. No API key errors

---

## 🐛 Troubleshooting

### "Secrets not found" Error

**Problem:** App can't find `.streamlit/secrets.toml`

**Solutions:**
1. Check file exists: `ls -la .streamlit/`
2. Check file name is exactly `secrets.toml` (not .txt)
3. Check file is in `.streamlit/` folder (not root)
4. Restart Streamlit server

### "Invalid API Key" Error

**Problem:** Credentials are wrong or malformed

**Solutions:**
1. Check for extra spaces in secrets.toml
2. Verify quotes are correct (use `"` not `'`)
3. For private_key, use triple quotes `"""`
4. Regenerate Firebase service account key
5. Regenerate OpenAI API key

### "Module not found" Error

**Problem:** Missing dependencies

**Solution:**
```bash
pip install -r requirements.txt
```

### Can't Create Account

**Problem:** Firebase authentication not enabled

**Solution:**
1. Firebase Console > Authentication
2. Sign-in method tab
3. Enable "Email/Password"

### Data Not Saving

**Problem:** Database rules or permissions

**Solutions:**
1. Firebase Console > Realtime Database
2. Rules tab
3. Use test mode rules:
```json
{
  "rules": {
    ".read": "auth != null",
    ".write": "auth != null"
  }
}
```

---

## 📝 Requirements.txt

Make sure you have:

```txt
streamlit>=1.28.0
firebase-admin>=6.2.0
pyrebase4>=4.6.0
openai>=1.3.0
python-dotenv>=1.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🔄 Migrating from Old Config

If you already had `firebase_config.py` with hardcoded values:

### Before:
```python
# firebase_config.py
FIREBASE_CONFIG = {
    "apiKey": "AIza...",
    # ...
}
```

### After:
```toml
# .streamlit/secrets.toml
[firebase]
apiKey = "AIza..."
# ...
```

The new `firebase_config.py` automatically reads from secrets!

---

## 🎯 Quick Checklist

Setup checklist:
- [ ] Created `.streamlit/secrets.toml`
- [ ] Added Firebase credentials
- [ ] Added OpenAI API key
- [ ] Added secrets.toml to .gitignore
- [ ] Tested locally
- [ ] Pushed to GitHub (without secrets!)
- [ ] Deployed to Streamlit Cloud
- [ ] Added secrets in Cloud dashboard
- [ ] Tested in production

---

## 💡 Tips

**For Multiple Environments:**

Create different secrets files:
- `.streamlit/secrets.dev.toml` (development)
- `.streamlit/secrets.prod.toml` (production)

Copy the right one:
```bash
cp .streamlit/secrets.dev.toml .streamlit/secrets.toml
```

**For Team Collaboration:**

1. Keep `secrets.toml.example` in Git (with dummy values)
2. Share actual secrets securely (1Password, LastPass, etc.)
3. Each team member creates their own `secrets.toml`

**For CI/CD:**

Use environment variables:
```bash
export OPENAI_API_KEY="sk-..."
export FIREBASE_API_KEY="AIza..."
```

The code falls back to environment variables if secrets aren't found.

---

## ✨ Benefits of Using Secrets

1. **Security:** Credentials never in Git
2. **Simplicity:** One file for all secrets
3. **Portability:** Same code works locally & cloud
4. **Team-friendly:** Each person has own secrets
5. **Safe commits:** Can't accidentally expose keys

You're all set! 🚀
