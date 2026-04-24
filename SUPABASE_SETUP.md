# KAB Banking System - Supabase Backend Setup Guide

## 📋 Overview

This guide helps you migrate the KAB Banking System from a local C program backend to **Supabase** - a scalable PostgreSQL database with built-in APIs, authentication, and real-time features.

### What is Supabase?
- PostgreSQL database hosted in the cloud
- Built-in REST API (no need for backend code)
- Real-time subscriptions
- Row-Level Security (RLS) for data protection
- Authentication system
- Storage for files

---

## 🚀 Quick Start (5 Steps)

### Step 1: Create a Supabase Account & Project

1. Go to https://supabase.com
2. Sign up / Sign in
3. Click **"New Project"**
4. Fill in:
   - **Name**: `kab-bank`
   - **Database Password**: Create a strong password
   - **Region**: Choose closest to you
5. Click **"Create new project"** (this takes 2-3 minutes)

### Step 2: Get Your API Credentials

1. In your Supabase dashboard, go to **Settings → API**
2. Copy these values:
   - **Project URL** (example: `https://xxxxx.supabase.co`)
   - **Anon Key** (the public key)
3. Keep these safe! You'll need them in Step 4.

### Step 3: Create Database Schema

1. In Supabase, go to **SQL Editor**
2. Click **"New Query"**
3. Copy and paste the entire content of `supabase_setup.sql`
4. Click **"Run"** (or press `Ctrl+Enter`)
5. You should see: `Success: 0 rows affected`

✅ Your database is now ready!

### Step 4: Set Up Your Backend

#### Option A: Using the New Supabase Backend (Recommended)

1. **Install dependencies:**
   ```bash
   pip install flask supabase-py python-dotenv
   ```

2. **Create `.env` file** (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env`** with your credentials:
   ```
   SUPABASE_URL=https://your-xxxxx.supabase.co
   SUPABASE_KEY=your_anon_key_here
   ADMIN_PASSWORD=admin123
   ```

4. **Run the server:**
   ```bash
   python server_supabase.py
   ```
   
   You should see:
   ```
   ============================================================
   KAB Banking System - Supabase Backend
   ============================================================
   Supabase URL: https://your-xxxxx.supabase.co
   Server running at http://localhost:5000
   ============================================================
   ```

5. **Open your browser** and go to: http://localhost:5000

✅ Your app is now using Supabase!

---

## 📊 Database Schema

### `accounts` Table
```sql
CREATE TABLE accounts (
    id BIGSERIAL PRIMARY KEY,
    account_number BIGINT UNIQUE NOT NULL,    -- 1001, 1002, ...
    holder_name VARCHAR(50) NOT NULL,          -- Account owner name
    balance DECIMAL(10, 2) NOT NULL,           -- Account balance
    pin VARCHAR(4) NOT NULL,                   -- 4-digit PIN
    created_at TIMESTAMP DEFAULT NOW(),        -- Account creation time
    updated_at TIMESTAMP DEFAULT NOW(),        -- Last update time
    is_deleted BOOLEAN DEFAULT FALSE           -- Soft delete flag
);
```

### `transactions` Table
```sql
CREATE TABLE transactions (
    id BIGSERIAL PRIMARY KEY,
    account_number BIGINT NOT NULL,            -- Link to accounts
    type VARCHAR(20) NOT NULL,                 -- DEPOSIT, WITHDRAWAL, TRANSFER_OUT, etc.
    amount DECIMAL(10, 2) NOT NULL,           -- Transaction amount
    timestamp TIMESTAMP DEFAULT NOW(),         -- When it happened
    details JSONB DEFAULT '{}'::jsonb         -- Additional info (JSON)
);
```

---

## 🔑 Environment Variables

Create a `.env` file with:

| Variable | Example | Description |
|----------|---------|-------------|
| `SUPABASE_URL` | `https://xxx.supabase.co` | Your Supabase project URL |
| `SUPABASE_KEY` | `eyJ0eX...` | Your anon key (from API settings) |
| `ADMIN_PASSWORD` | `admin123` | Password for admin login |
| `FLASK_ENV` | `development` | Flask environment |
| `FLASK_DEBUG` | `True` | Enable debug mode |

⚠️ **Never commit `.env` to GitHub!** It contains secrets.

---

## 🔒 Security Best Practices

### 1. Protect Your Keys
- Never commit `.env` to git
- Add `.env` to `.gitignore`:
  ```bash
  echo ".env" >> .gitignore
  ```

### 2. Use Anon Key Wisely
- The **Anon Key** is public (safe in frontend)
- Use **Service Role Key** only on backend for admin operations
- Never expose Service Role Key to frontend

### 3. Set Up Row-Level Security (Optional)
```sql
-- Uncomment in supabase_setup.sql to enable:
ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "View own account" ON accounts
  FOR SELECT USING (true);  -- Add auth logic later
```

---

## 🔄 Migration from Old System

If you had data in the old system:

1. **Export from old system** (get accounts and transactions)
2. **Insert into Supabase:**
   ```sql
   INSERT INTO accounts (account_number, holder_name, balance, pin)
   VALUES (1001, 'John Doe', 50000, '1234');
   
   INSERT INTO transactions (account_number, type, amount)
   VALUES (1001, 'CREATED', 50000);
   ```

---

## 🐛 Troubleshooting

### "Connection refused"
- Check your `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Make sure they're not empty or malformed

### "Table does not exist"
- Run the SQL from `supabase_setup.sql` in Supabase SQL Editor
- Verify the table appears in Database → Tables

### "Invalid API key"
- Go to Supabase → Settings → API
- Make sure you copied the correct key

### "CORS error in browser"
- This is normal for development
- In production, set proper CORS headers in Flask

---

## 📚 Useful Links

- **Supabase Docs**: https://supabase.com/docs
- **Supabase Python Client**: https://github.com/supabase/supabase-py
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Flask Docs**: https://flask.palletsprojects.com/

---

## ✅ What Works Now

- ✅ Account creation
- ✅ Deposits
- ✅ Withdrawals
- ✅ Transfers
- ✅ Balance inquiries
- ✅ Account deletion
- ✅ Admin login
- ✅ Transaction history
- ✅ List all accounts

---

## 🎯 Next Steps

1. ✅ Create Supabase account
2. ✅ Set up database schema
3. ✅ Configure `.env` file
4. ✅ Run `server_supabase.py`
5. 🔄 Test the app at http://localhost:5000
6. 📤 Deploy to production (Vercel, Railway, Heroku, etc.)

---

## 📞 Support

If you have issues:
1. Check Supabase Status: https://status.supabase.com
2. Read error messages carefully
3. Check `.env` file is correct
4. Review Supabase documentation

Good luck! 🚀
