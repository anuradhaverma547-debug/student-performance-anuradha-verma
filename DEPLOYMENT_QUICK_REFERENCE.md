# 🚀 Quick Reference: Deployment Commands

## Copy & Paste Command Sequence

### **Phase 1: Local Git Setup**
```powershell
cd c:\Users\HP\OneDrive\Desktop\student-performance-app
git init
git config --global user.name "Anuradha Verma"
git config --global user.email "your-email@example.com"
git add .
git commit -m "Initial commit: Student performance ML analytics app with Streamlit UI, linear regression model, and interactive dashboards"
```

### **Phase 2: Link to GitHub**
```powershell
git remote add origin https://github.com/YOUR-USERNAME/student-performance-analytics.git
git branch -M main
git push -u origin main
```

---

## 📋 GitHub Setup (Web)

1. **Create Repo**: https://github.com/new
   - Name: `student-performance-analytics`
   - Visibility: **Public**
   - ❌ Don't initialize

2. **Copy Commands** from GitHub → Run in PowerShell

---

## 🌐 Streamlit Cloud Setup (Web)

1. **Sign Up**: https://share.streamlit.io
   - Click "Sign in with GitHub"

2. **Deploy New App**:
   - Click "New app"
   - Select: `YOUR-USERNAME/student-performance-analytics`
   - Branch: `main`
   - Main file: `Model/app.py`
   - App URL: `anuradhaverma-student-performance`

3. **Wait** for deployment (2-5 min)

---

## ✅ Final URLs

```
GitHub:    https://github.com/YOUR-USERNAME/student-performance-analytics
Streamlit: https://anuradhaverma-student-performance.streamlit.app/
```

---

## 💡 Auto-Deploy Magic

After first deployment, every `git push` auto-deploys!

```powershell
git add .
git commit -m "Your message"
git push origin main
# Changes live in 2-3 minutes automatically!
```

---

**See DEPLOYMENT_GUIDE.md for detailed step-by-step instructions with troubleshooting!**
