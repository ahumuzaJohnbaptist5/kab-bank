# server.py
# Run with:  python server.py
# Requires:  pip install flask
#
# This file is the bridge between the web browser and your C program.
# It receives HTTP requests from the browser, calls banking_web.exe,
# and sends the JSON response back.

from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__)

# Path to your compiled C executable
C_PROGRAM = os.path.join(os.path.dirname(__file__), "banking_web.exe")


def run_c(args):
    """
    Calls banking_web.exe with the given arguments.
    Returns the parsed JSON output as a Python dict or list.
    """
    try:
        result = subprocess.run(
            [C_PROGRAM] + [str(a) for a in args],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout.strip()
        if not output:
            return {"status": "error", "message": "No response from C program"}
        import json
        return json.loads(output)
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "C program timed out"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── Serve the frontend ─────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# ── API Routes ─────────────────────────────────────────────

@app.route("/api/create", methods=["POST"])
def create():
    data = request.json
    return jsonify(run_c([
        "create",
        data["name"],
        data["deposit"],
        data["pin"]
    ]))


@app.route("/api/deposit", methods=["POST"])
def deposit():
    data = request.json
    return jsonify(run_c([
        "deposit",
        data["accountNumber"],
        data["amount"]
    ]))


@app.route("/api/withdraw", methods=["POST"])
def withdraw():
    data = request.json
    return jsonify(run_c([
        "withdraw",
        data["accountNumber"],
        data["amount"],
        data["pin"]
    ]))


@app.route("/api/balance", methods=["POST"])
def balance():
    data = request.json
    return jsonify(run_c([
        "balance",
        data["accountNumber"],
        data["pin"]
    ]))


@app.route("/api/transfer", methods=["POST"])
def transfer():
    data = request.json
    return jsonify(run_c([
        "transfer",
        data["fromAccount"],
        data["toAccount"],
        data["amount"],
        data["pin"]
    ]))


@app.route("/api/list", methods=["GET"])
def list_accounts():
    return jsonify(run_c(["list"]))


@app.route("/api/history", methods=["GET"])
def history():
    return jsonify(run_c(["history"]))


@app.route("/api/delete", methods=["POST"])
def delete():
    data = request.json
    return jsonify(run_c([
        "delete",
        data["accountNumber"],
        data["pin"]
    ]))


@app.route("/api/admin_login", methods=["POST"])
def admin_login():
    data = request.json
    return jsonify(run_c([
        "admin_login",
        data["password"]
    ]))


# ── Start server ───────────────────────────────────────────

if __name__ == "__main__":
    print("KAB Banking System running at http://localhost:5000")
    app.run(debug=True, port=5000)
