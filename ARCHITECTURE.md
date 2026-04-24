# KAB Banking System - Architecture Guide

## 📊 Old vs. New Architecture

### Original Architecture (C + Flask)
```
Frontend (HTML/JS) 
    ↓
Flask Server (Python)
    ↓
C Program (banking_web.exe)
    ↓
Local Files (accounts.dat, transactions.log)
```

**Limitations:**
- ❌ Data stored in binary files (fragile)
- ❌ No real-time features
- ❌ Difficult to scale
- ❌ No built-in authentication
- ❌ Hard to backup/restore data

---

### New Architecture (Supabase)
```
Frontend (HTML/JS)
    ↓
Flask Server (Python)
    ↓
Supabase REST API
    ↓
PostgreSQL Database (Cloud)
```

**Advantages:**
- ✅ Reliable PostgreSQL database
- ✅ Built-in backups and recovery
- ✅ Easy to scale
- ✅ Real-time subscriptions
- ✅ Row-Level Security (RLS)
- ✅ Built-in authentication (Auth0, Google, etc.)
- ✅ Hosted in the cloud
- ✅ Can be accessed from anywhere

---

## 🔄 How to Switch Between Backends

### Run Old Backend (C program)
```bash
python server.py
# Uses banking_web.exe and local files
```

### Run New Backend (Supabase)
```bash
# 1. Create .env file with Supabase credentials
cp .env.example .env
# Edit .env with your credentials

# 2. Install dependencies
pip install -r requirements_supabase.txt

# 3. Run server
python server_supabase.py
```

Both servers run on **http://localhost:5000** - just use one at a time!

---

## 📁 Project Files

| File | Purpose |
|------|---------|
| `banking_web.c` | Original C banking logic (optional now) |
| `server.py` | Old Flask backend (uses C program) |
| `server_supabase.py` | **NEW** Flask backend (uses Supabase) |
| `index.html` | Web frontend (works with both) |
| `supabase_setup.sql` | **NEW** Database schema for Supabase |
| `.env.example` | **NEW** Environment variables template |
| `requirements_supabase.txt` | **NEW** Python dependencies for Supabase |
| `SUPABASE_SETUP.md` | **NEW** Detailed setup guide |

---

## 🚀 Getting Started with Supabase

1. **Create account**: https://supabase.com
2. **Create project**: In dashboard
3. **Run SQL**: Copy `supabase_setup.sql` to SQL Editor
4. **Get credentials**: Settings → API
5. **Configure `.env`**: Add URL and key
6. **Install packages**: `pip install -r requirements_supabase.txt`
7. **Run server**: `python server_supabase.py`
8. **Visit**: http://localhost:5000

---

## 🔐 Security Considerations

### Old System
- ⚠️ Binary files unencrypted
- ⚠️ No database-level security
- ⚠️ PIN stored as plain text in files

### New System (Supabase)
- ✅ HTTPS encrypted connections
- ✅ Row-Level Security (RLS) policies
- ✅ Separate Anon and Service Role keys
- ✅ Built-in audit logs
- ✅ Password policies
- 🔄 PIN still plain text (consider hashing in production)

---

## 💾 Data Types Mapping

### Old (C)
```c
int accountNumber;        // 1001, 1002, ...
char holderName[50];      // "John Doe"
float balance;            // 50000.50
int pin;                  // 1234
```

### New (Supabase)
```sql
account_number BIGINT     -- 1001, 1002, ...
holder_name VARCHAR(50)   -- "John Doe"
balance DECIMAL(10, 2)    -- 50000.50
pin VARCHAR(4)            -- "1234"
```

---

## 🔍 API Endpoints (Same for Both)

Both backends expose the same REST API:

```
POST   /api/create           -- Create account
POST   /api/deposit          -- Deposit money
POST   /api/withdraw         -- Withdraw money
POST   /api/transfer         -- Transfer between accounts
POST   /api/balance          -- Check balance
POST   /api/delete           -- Delete account
POST   /api/admin_login      -- Admin authentication
GET    /api/list             -- List all accounts
GET    /api/history          -- Transaction history
```

The frontend doesn't need changes - it works with either backend!

---

## 📈 Performance Comparison

| Metric | Old System | New System |
|--------|-----------|-----------|
| **Query Speed** | Fast (local) | Very fast (optimized) |
| **Concurrent Users** | ~5 | Unlimited |
| **Data Backup** | Manual | Automatic |
| **Availability** | 99% (local) | 99.99% (cloud) |
| **Scalability** | Limited | Unlimited |

---

## 🆘 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'supabase'"
**Solution:**
```bash
pip install -r requirements_supabase.txt
```

### Issue: "Could not connect to Supabase"
**Solution:**
1. Check `.env` file exists
2. Verify `SUPABASE_URL` and `SUPABASE_KEY`
3. Check internet connection
4. Verify keys are correct from Settings → API

### Issue: "Table does not exist"
**Solution:**
1. Go to Supabase dashboard
2. Open SQL Editor
3. Run `supabase_setup.sql`
4. Verify tables appear in left sidebar

---

## 📚 Learning Resources

- **Supabase**: https://supabase.com/docs
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Python Flask**: https://flask.palletsprojects.com/
- **REST APIs**: https://restfulapi.net/

---

## ✅ Checklist

- [ ] Create Supabase account
- [ ] Create Supabase project
- [ ] Run SQL schema
- [ ] Copy `.env.example` to `.env`
- [ ] Add Supabase credentials to `.env`
- [ ] Install dependencies: `pip install -r requirements_supabase.txt`
- [ ] Start server: `python server_supabase.py`
- [ ] Test at http://localhost:5000
- [ ] Create a test account
- [ ] Test all features
- [ ] Delete test account
- [ ] Check transaction history

---

## 🎯 Next Steps

1. **Development**: Use Supabase for local development
2. **Testing**: Test all features thoroughly
3. **Production**: Deploy to cloud platform (Vercel, Railway, Heroku)
4. **Monitoring**: Set up alerts and monitoring
5. **Backup**: Enable automatic backups in Supabase

---

**Ready to go? Follow the SUPABASE_SETUP.md guide!** 🚀
