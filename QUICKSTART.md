# KAB Banking System - Complete Setup Guide

## 🎯 What's New?

Your KAB Banking System now has **two backend options**:

### Option 1: Local Backend (Original)
- Uses local C program and binary files
- Good for learning and local testing
- Run: `python server.py`

### Option 2: Cloud Backend with Supabase (NEW!)
- Uses cloud PostgreSQL database
- Scalable and production-ready
- More features and security
- Run: `python server_supabase.py`

---

## 🚀 Quick Start (Choose One)

### 🟢 Option 1: Run Locally (Original)

```bash
# Already set up, just run:
python server.py

# Then visit: http://localhost:5000
```

**Good for:**
- Learning
- Development without internet
- Testing locally

---

### 🔵 Option 2: Use Supabase Cloud (Recommended)

#### Step 1: Create Supabase Account (2 min)
1. Go to https://supabase.com
2. Click **Sign Up**
3. Create account with email or GitHub
4. Create a **New Project**

#### Step 2: Get Your Credentials (1 min)
1. Open your project
2. Go to **Settings → API**
3. Copy:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **Anon Key** (the public key)

#### Step 3: Set Up Your Computer (2 min)

**Windows:**
```bash
# Just double-click this file:
setup_supabase.bat
```

**Mac/Linux:**
```bash
# Run these commands:
cp .env.example .env
pip install -r requirements_supabase.txt
python server_supabase.py
```

#### Step 4: Configure Your Credentials (1 min)
1. Open `.env` file in any text editor
2. Paste your Supabase URL and Key:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_anon_key_here
   ```
3. Save the file

#### Step 5: Create Database Schema (1 min)
1. In Supabase, open **SQL Editor**
2. Click **New Query**
3. Copy entire content of `supabase_setup.sql`
4. Click **Run**

✅ Done! Your database is ready.

#### Step 6: Start Your App (1 min)
```bash
python server_supabase.py
```

Visit: http://localhost:5000

---

## 📊 Comparison

| Feature | Local | Supabase |
|---------|-------|----------|
| **Setup Time** | 1 min | 10 min |
| **Internet Required** | ❌ No | ✅ Yes |
| **Scalability** | ⚠️ Limited | ✅ Unlimited |
| **Backups** | Manual | Automatic |
| **Real-time** | ❌ No | ✅ Yes |
| **Cost** | Free | Free tier included |

---

## 📁 New Files

| File | Purpose |
|------|---------|
| `server_supabase.py` | Supabase backend |
| `supabase_setup.sql` | Database schema |
| `.env.example` | Credentials template |
| `.env` | Your credentials (secret!) |
| `requirements_supabase.txt` | Python packages |
| `setup_supabase.bat` | Windows setup script |
| `SUPABASE_SETUP.md` | Detailed guide |
| `ARCHITECTURE.md` | Technical details |

---

## ✅ Features

Both backends support:
- ✅ Create accounts
- ✅ Deposit money
- ✅ Withdraw money
- ✅ Transfer funds
- ✅ Check balance
- ✅ Delete account
- ✅ Admin login
- ✅ Transaction history
- ✅ View all accounts

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: flask"
**Solution:**
```bash
pip install flask supabase-py python-dotenv
```

### Problem: "Could not connect to Supabase"
**Solution:**
1. Check `.env` file exists
2. Verify SUPABASE_URL starts with `https://`
3. Check SUPABASE_KEY is not empty
4. Verify internet connection

### Problem: "Table 'accounts' does not exist"
**Solution:**
1. In Supabase, go to SQL Editor
2. Run all commands from `supabase_setup.sql`
3. Check left sidebar for `accounts` table

---

## 📚 Documentation

- **Full Setup Guide**: Read `SUPABASE_SETUP.md`
- **Architecture Info**: Read `ARCHITECTURE.md`
- **Supabase Docs**: https://supabase.com/docs
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

## 🔒 Security Tips

⚠️ **IMPORTANT:**
1. Never share your `.env` file
2. Never commit `.env` to GitHub
3. Add `.env` to `.gitignore`
4. Change `ADMIN_PASSWORD` in production
5. Use strong account passwords

---

## 📊 Next Steps

1. **Choose your backend** (Local or Supabase)
2. **Follow setup for that option** (above)
3. **Test all features** at http://localhost:5000
4. **Create test account** and try all operations
5. **Check transaction history**
6. **Deploy** when ready

---

## 🎓 Learning

Want to understand more?
- **Local Backend**: Uses C for business logic
- **Supabase Backend**: Uses PostgreSQL + REST API
- **Frontend**: Same HTML/JavaScript for both

---

## 💬 Need Help?

1. Check the **Troubleshooting** section above
2. Read **SUPABASE_SETUP.md** for detailed steps
3. Review **ARCHITECTURE.md** for technical details
4. Visit https://supabase.com/docs for more help

---

**Ready? Start with Step 1 above!** 🚀
