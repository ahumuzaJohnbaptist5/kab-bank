-- ============================================================
-- KAB Bank - Supabase Database Schema
-- Run this SQL in your Supabase SQL Editor
-- ============================================================

-- Create accounts table
CREATE TABLE accounts (
    id BIGSERIAL PRIMARY KEY,
    account_number BIGINT UNIQUE NOT NULL,
    holder_name VARCHAR(50) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0,
    pin VARCHAR(4) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE
);

-- Create transactions table
CREATE TABLE transactions (
    id BIGSERIAL PRIMARY KEY,
    account_number BIGINT NOT NULL REFERENCES accounts(account_number),
    type VARCHAR(20) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    details JSONB DEFAULT '{}'::jsonb
);

-- Create indexes for performance
CREATE INDEX idx_accounts_account_number ON accounts(account_number);
CREATE INDEX idx_accounts_holder_name ON accounts(holder_name);
CREATE INDEX idx_transactions_account_number ON transactions(account_number);
CREATE INDEX idx_transactions_timestamp ON transactions(timestamp DESC);

-- Create a sequence for account numbers starting at 1001
CREATE SEQUENCE account_number_seq START WITH 1001 INCREMENT BY 1;

-- Insert initial account if needed
-- INSERT INTO accounts (account_number, holder_name, balance, pin) 
-- VALUES (nextval('account_number_seq'), 'Test Account', 50000, '1234');

-- Row-Level Security (RLS) - Optional but recommended
-- ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

-- Create policies (optional - for security)
-- CREATE POLICY "Users can only view their own account"
-- ON accounts FOR SELECT
-- USING (true);  -- You can add auth logic here later

COMMIT;
