# server_supabase.py
# KAB Banking System - Supabase Backend
# Run with: pip install flask supabase-py python-dotenv
#           python server_supabase.py

from flask import Flask, request, jsonify, send_from_directory
from supabase import create_client, Client
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ══════════════════════════════════════════════════════════════
# SUPABASE CONFIGURATION
# ══════════════════════════════════════════════════════════════
# Set these environment variables or update .env file:
#   SUPABASE_URL=your_project_url
#   SUPABASE_KEY=your_anon_key

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your_anon_key_here")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════

def get_next_account_number():
    """Get the next account number from sequence"""
    try:
        result = supabase.rpc('nextval', {'seq_name': 'account_number_seq'}).execute()
        return result.data
    except:
        # Fallback: get max account_number and add 1
        data = supabase.table('accounts').select('account_number').order('account_number', desc=True).limit(1).execute()
        if data.data:
            return data.data[0]['account_number'] + 1
        return 1001

def log_transaction(account_number, trans_type, amount, details=None):
    """Log a transaction"""
    try:
        supabase.table('transactions').insert({
            'account_number': account_number,
            'type': trans_type,
            'amount': float(amount),
            'details': details or {}
        }).execute()
    except Exception as e:
        print(f"Error logging transaction: {e}")

def verify_account_pin(account_number, pin):
    """Verify if PIN is correct for account"""
    try:
        data = supabase.table('accounts').select('pin').eq('account_number', account_number).eq('is_deleted', False).execute()
        if not data.data:
            return False, "Account not found"
        if str(data.data[0]['pin']) != str(pin):
            return False, "Incorrect PIN - access denied"
        return True, None
    except Exception as e:
        return False, str(e)

# ══════════════════════════════════════════════════════════════
# SERVE THE FRONTEND
# ══════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# ══════════════════════════════════════════════════════════════
# API ROUTES
# ══════════════════════════════════════════════════════════════

@app.route("/api/create", methods=["POST"])
def create_account():
    try:
        data = request.json
        name = data.get("name", "").strip()
        deposit = float(data.get("deposit", 0))
        pin = str(data.get("pin", ""))

        # Validation
        if not name:
            return jsonify({"status": "error", "message": "Name cannot be empty"}), 400
        if deposit < 0:
            return jsonify({"status": "error", "message": "Initial deposit cannot be negative"}), 400
        if len(pin) != 4 or not pin.isdigit():
            return jsonify({"status": "error", "message": "PIN must be exactly 4 digits"}), 400

        account_number = get_next_account_number()

        result = supabase.table('accounts').insert({
            'account_number': account_number,
            'holder_name': name,
            'balance': float(deposit),
            'pin': pin
        }).execute()

        log_transaction(account_number, 'CREATED', deposit)

        return jsonify({
            "status": "ok",
            "accountNumber": account_number,
            "name": name,
            "balance": float(deposit)
        }), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/deposit", methods=["POST"])
def deposit():
    try:
        data = request.json
        account_number = int(data.get("accountNumber"))
        amount = float(data.get("amount", 0))

        # Validation
        if amount <= 0:
            return jsonify({"status": "error", "message": "Deposit amount must be greater than zero"}), 400

        # Get account
        account_data = supabase.table('accounts').select('*').eq('account_number', account_number).eq('is_deleted', False).execute()
        if not account_data.data:
            return jsonify({"status": "error", "message": "Account not found - please verify account number"}), 404

        account = account_data.data[0]
        new_balance = float(account['balance']) + amount

        # Update balance
        supabase.table('accounts').update({
            'balance': new_balance,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('account_number', account_number).execute()

        log_transaction(account_number, 'DEPOSIT', amount)

        return jsonify({
            "status": "ok",
            "accountHolder": account['holder_name'],
            "balance": new_balance,
            "message": f"Successfully deposited UGX {amount:.2f} to account"
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/withdraw", methods=["POST"])
def withdraw():
    try:
        data = request.json
        account_number = int(data.get("accountNumber"))
        amount = float(data.get("amount", 0))
        pin = str(data.get("pin", ""))

        # Verify PIN
        pin_valid, error_msg = verify_account_pin(account_number, pin)
        if not pin_valid:
            return jsonify({"status": "error", "message": error_msg}), 401

        # Validation
        if amount <= 0:
            return jsonify({"status": "error", "message": "Withdrawal amount must be greater than zero"}), 400

        # Get account
        account_data = supabase.table('accounts').select('*').eq('account_number', account_number).eq('is_deleted', False).execute()
        if not account_data.data:
            return jsonify({"status": "error", "message": "Account not found - please verify account number"}), 404

        account = account_data.data[0]
        if float(account['balance']) < amount:
            return jsonify({"status": "error", "message": "Insufficient funds - cannot withdraw more than balance"}), 400

        new_balance = float(account['balance']) - amount

        # Update balance
        supabase.table('accounts').update({
            'balance': new_balance,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('account_number', account_number).execute()

        log_transaction(account_number, 'WITHDRAWAL', amount)

        return jsonify({
            "status": "ok",
            "accountHolder": account['holder_name'],
            "balance": new_balance,
            "message": f"Successfully withdrew UGX {amount:.2f} from account"
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/balance", methods=["POST"])
def balance():
    try:
        data = request.json
        account_number = int(data.get("accountNumber"))
        pin = str(data.get("pin", ""))

        # Verify PIN
        pin_valid, error_msg = verify_account_pin(account_number, pin)
        if not pin_valid:
            return jsonify({"status": "error", "message": error_msg}), 401

        # Get account
        account_data = supabase.table('accounts').select('*').eq('account_number', account_number).eq('is_deleted', False).execute()
        if not account_data.data:
            return jsonify({"status": "error", "message": "Account not found - please verify account number"}), 404

        account = account_data.data[0]
        return jsonify({
            "status": "ok",
            "accountNumber": account['account_number'],
            "name": account['holder_name'],
            "balance": float(account['balance'])
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/transfer", methods=["POST"])
def transfer():
    try:
        data = request.json
        from_account = int(data.get("fromAccount"))
        to_account = int(data.get("toAccount"))
        amount = float(data.get("amount", 0))
        pin = str(data.get("pin", ""))

        # Verify PIN
        pin_valid, error_msg = verify_account_pin(from_account, pin)
        if not pin_valid:
            return jsonify({"status": "error", "message": error_msg}), 401

        # Validation
        if from_account == to_account:
            return jsonify({"status": "error", "message": "Cannot transfer to same account"}), 400
        if amount <= 0:
            return jsonify({"status": "error", "message": "Transfer amount must be greater than zero"}), 400

        # Get both accounts
        from_data = supabase.table('accounts').select('*').eq('account_number', from_account).eq('is_deleted', False).execute()
        to_data = supabase.table('accounts').select('*').eq('account_number', to_account).eq('is_deleted', False).execute()

        if not from_data.data:
            return jsonify({"status": "error", "message": "Source account not found - please verify account number"}), 404
        if not to_data.data:
            return jsonify({"status": "error", "message": "Destination account not found - please verify recipient account"}), 404

        from_account_data = from_data.data[0]
        to_account_data = to_data.data[0]

        if float(from_account_data['balance']) < amount:
            return jsonify({"status": "error", "message": "Insufficient funds for this transfer"}), 400

        # Perform transfer
        new_from_balance = float(from_account_data['balance']) - amount
        new_to_balance = float(to_account_data['balance']) + amount

        supabase.table('accounts').update({
            'balance': new_from_balance,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('account_number', from_account).execute()

        supabase.table('accounts').update({
            'balance': new_to_balance,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('account_number', to_account).execute()

        log_transaction(from_account, 'TRANSFER_OUT', amount, {'to_account': to_account})
        log_transaction(to_account, 'TRANSFER_IN', amount, {'from_account': from_account})

        return jsonify({
            "status": "ok",
            "newBalance": new_from_balance,
            "message": f"Transfer of UGX {amount:.2f} successful to {to_account_data['holder_name']}",
            "recipientName": to_account_data['holder_name']
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/delete", methods=["POST"])
def delete_account():
    try:
        data = request.json
        account_number = int(data.get("accountNumber"))
        pin = str(data.get("pin", ""))

        # Verify PIN
        pin_valid, error_msg = verify_account_pin(account_number, pin)
        if not pin_valid:
            return jsonify({"status": "error", "message": error_msg}), 401

        # Get account
        account_data = supabase.table('accounts').select('*').eq('account_number', account_number).eq('is_deleted', False).execute()
        if not account_data.data:
            return jsonify({"status": "error", "message": "Account not found"}), 404

        account = account_data.data[0]

        # Soft delete
        supabase.table('accounts').update({
            'is_deleted': True,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('account_number', account_number).execute()

        log_transaction(account_number, 'ACCOUNT_DELETED', float(account['balance']))

        return jsonify({
            "status": "ok",
            "message": f"Account for {account['holder_name']} (Acc #{account_number}) has been deleted successfully"
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/list", methods=["GET"])
def list_accounts():
    try:
        data = supabase.table('accounts').select('account_number, holder_name, balance').eq('is_deleted', False).execute()
        accounts = [
            {
                "accountNumber": acc['account_number'],
                "name": acc['holder_name'],
                "balance": float(acc['balance'])
            }
            for acc in data.data
        ]
        return jsonify(accounts), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/history", methods=["GET"])
def history():
    try:
        data = supabase.table('transactions').select('*').order('timestamp', desc=True).limit(100).execute()
        transactions = [
            {
                "account": trans['account_number'],
                "type": trans['type'],
                "amount": float(trans['amount']),
                "timestamp": trans['timestamp']
            }
            for trans in data.data
        ]
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/admin_login", methods=["POST"])
def admin_login():
    try:
        data = request.json
        password = data.get("password", "")
        
        # Simple admin password - change this in production!
        ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
        
        if password == ADMIN_PASSWORD:
            return jsonify({
                "status": "ok",
                "message": "Admin login successful",
                "authenticated": True
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid admin password",
                "authenticated": False
            }), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# ══════════════════════════════════════════════════════════════
# START SERVER
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("KAB Banking System - Supabase Backend")
    print("=" * 60)
    print(f"Supabase URL: {SUPABASE_URL}")
    print("Server running at http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)
