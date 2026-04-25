# KAB Bank — University E-Banking System

![KAB Bank](https://img.shields.io/badge/KAB%20Bank-E--Banking-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A full-stack university e-banking web application built for managing student accounts, tuition payments, transfers, transactions, and financial services within a university environment.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Database Schema](#database-schema)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

KAB Bank is a university e-banking system designed to digitize and streamline financial operations for students, staff, and faculty. It supports account management, fund transfers, transaction history, tuition fee payments, card management, and more — all accessible through a clean web interface.

> Built as part of a university project (Course: A25.BCS1205-24)

---

## Features

- **Dashboard** — Overview of account balance, recent transactions, and quick actions
- **Accounts** — View and manage university-linked bank accounts
- **Transfers** — Internal and external fund transfers
- **Transactions** — Full transaction history with filters
- **Profile** — Personal and university details management
- **Cards** — Virtual/physical card management
- **Support** — In-app help and ticket system
- **Security** — 2FA, session management, password controls
- **Notifications** — Real-time alerts for account activity
- **Authentication** — Secure login with role-based access (Student / Staff / Admin)

---

## Tech Stack

### Frontend
| Technology | Purpose |
|---|---|
| React.js | UI framework |
| React Router | Client-side routing |
| Tailwind CSS / CSS Modules | Styling |
| Axios | HTTP requests to backend API |

### Backend
| Technology | Purpose |
|---|---|
| C (mongoose / libmicrohttpd) | Core HTTP application server |
| C Ledger Engine | Double-entry accounting, transaction processing |
| libpq | PostgreSQL client for C |
| OpenSSL | TLS encryption and JWT signing |
| cJSON | JSON parsing in C |
| libcurl | External API integrations |

### Database & Infrastructure
| Technology | Purpose |
|---|---|
| PostgreSQL | Primary database (accounts, ledger, users) |
| Supabase | Database hosting and Auth |
| Redis | Session cache and rate limiting |
| Nginx | Reverse proxy and static file serving |

---

## Architecture

```
┌─────────────────────────────────────┐
│         Browser (React App)         │
│   Dashboard · Accounts · Transfers  │
└──────────────┬──────────────────────┘
               │ HTTPS / REST API
┌──────────────▼──────────────────────┐
│           Nginx (Reverse Proxy)     │
│   SSL termination · Static files    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│       C Application Server          │
│  HTTP Router · Ledger Engine        │
│  Transaction Processor · Auth       │
│  Reconciliation · Fraud Detection   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│          Data Layer                 │
│  PostgreSQL · Redis · Audit Logs    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│       External Integrations         │
│  MTN/Airtel Mobile Money · SMTP     │
│  Student Info System (SIS) · URA    │
└─────────────────────────────────────┘
```

---

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Node.js `>= 18.x`
- GCC (C compiler) `>= 11`
- PostgreSQL `>= 14`
- Redis `>= 7`
- Nginx
- `libpq-dev`, `libssl-dev`, `libcurl4-openssl-dev`

### 1. Clone the repository

```bash
git clone https://github.com/ahumuzaJohnb/kab-bank.git
cd kab-bank
```

### 2. Install frontend dependencies

```bash
cd client
npm install
```

### 3. Build the C backend

```bash
cd server
make build
# or manually:
gcc -o kab_server main.c ledger.c auth.c routes.c \
    -lpq -lssl -lcrypto -lcurl -lmicrohttpd \
    -I./include -Wall -O2
```

### 4. Set up the database

```bash
psql -U postgres -c "CREATE DATABASE kabbank;"
psql -U postgres -d kabbank -f db/schema.sql
psql -U postgres -d kabbank -f db/seed.sql
```

### 5. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your values (see Environment Variables section)
```

### 6. Run the application

```bash
# Start the C backend server
./server/kab_server

# Start the React frontend (development)
cd client && npm run dev

# Or build for production
cd client && npm run build
```

The app will be available at `http://localhost:5000`

---

## Project Structure

```
kab-bank/
├── client/                  # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Dashboard, Accounts, Transfers, etc.
│   │   ├── hooks/           # Custom React hooks
│   │   ├── services/        # API call functions
│   │   └── App.jsx
│   └── package.json
│
├── server/                  # C backend
│   ├── main.c               # Entry point, HTTP server setup
│   ├── routes.c             # API route handlers
│   ├── ledger.c             # Double-entry ledger engine
│   ├── auth.c               # JWT auth middleware
│   ├── transactions.c       # Transaction processing
│   ├── reconciliation.c     # Balance reconciliation
│   ├── fraud.c              # Fraud detection rules
│   ├── include/             # Header files
│   └── Makefile
│
├── db/
│   ├── schema.sql           # Database schema
│   └── seed.sql             # Sample/test data
│
├── nginx/
│   └── kab_bank.conf        # Nginx config
│
├── .env.example
├── README.md
└── LICENSE
```

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/logout` | User logout |
| POST | `/api/auth/refresh` | Refresh JWT token |
| POST | `/api/auth/2fa/verify` | Verify 2FA code |

### Accounts
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/accounts` | Get all user accounts |
| GET | `/api/accounts/:id` | Get account details |
| GET | `/api/accounts/:id/balance` | Get account balance |

### Transfers
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/transfers` | Initiate a transfer |
| GET | `/api/transfers/:id` | Get transfer status |

### Transactions
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/transactions` | Get transaction history |
| GET | `/api/transactions/:id` | Get single transaction |

### Profile
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/profile` | Get user profile |
| PUT | `/api/profile` | Update profile |
| PUT | `/api/profile/photo` | Update profile photo |

---

## Environment Variables

Create a `.env` file in the root directory:

```env
# Server
PORT=8080
ENV=development

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=kabbank
DB_USER=postgres
DB_PASSWORD=your_password

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET=your_jwt_secret_key
JWT_EXPIRY=3600

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password

# Mobile Money
MTN_API_KEY=your_mtn_key
AIRTEL_API_KEY=your_airtel_key
```

---

## Database Schema

Core tables:

```sql
-- Users table
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    university_id VARCHAR(20) UNIQUE NOT NULL,
    full_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(100) UNIQUE NOT NULL,
    role        VARCHAR(20) CHECK (role IN ('student','staff','admin')),
    created_at  TIMESTAMP DEFAULT NOW()
);

-- Accounts table
CREATE TABLE accounts (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(id),
    account_no  VARCHAR(20) UNIQUE NOT NULL,
    type        VARCHAR(20) CHECK (type IN ('savings','current')),
    balance     BIGINT DEFAULT 0,   -- stored in UGX smallest unit
    status      VARCHAR(20) DEFAULT 'active',
    created_at  TIMESTAMP DEFAULT NOW()
);

-- Ledger (double-entry)
CREATE TABLE ledger_entries (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id  UUID REFERENCES accounts(id),
    type        VARCHAR(10) CHECK (type IN ('debit','credit')),
    amount      BIGINT NOT NULL,
    balance     BIGINT NOT NULL,
    reference   VARCHAR(64),
    description TEXT,
    created_at  TIMESTAMP DEFAULT NOW()
);
```

---

## Security

- All passwords hashed with **bcrypt**
- JWT tokens with short expiry + refresh token rotation
- **2FA** via TOTP (Google Authenticator compatible)
- All API endpoints protected with auth middleware
- Rate limiting on login and transfer endpoints
- Input validation and SQL injection prevention via parameterized queries
- HTTPS enforced via Nginx + SSL certificates
- Session invalidation on logout

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

> Built with ❤️ for Kabale University | Course A25.BCS1205-24
