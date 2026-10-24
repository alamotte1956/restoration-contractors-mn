from flask import Flask, request
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_PATH = "consumer.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, phone TEXT, email TEXT, zip TEXT,
                service_type TEXT, details TEXT, created_at TEXT, status TEXT DEFAULT 'new'
            );
        """)

init_db()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Best Contractors Twin Cities — One Pro. No Shared Leads.</title>
<style>
body{font-family:system-ui,sans-serif;margin:0;background:#f8fafc;color:#1e293b}
.hero{background:linear-gradient(135deg,#0f172a,#1e40af);color:#fff;padding:70px 20px;text-align:center}
.container{max-width:680px;margin:40px auto;padding:0 20px}
.card{background:#fff;border-radius:12px;padding:32px;box-shadow:0 4px 24px rgba(0,0,0,.08)}
input,select,textarea{width:100%;padding:12px;margin:8px 0;border:1px solid #cbd5e1;border-radius:8px;box-sizing:border-box}
button{width:100%;background:#0ea5e9;color:#fff;border:none;padding:16px;border-radius:8px;font-size:18px;cursor:pointer}
.steps{display:flex;gap:16px;margin:36px 0;text-align:center}
.step{flex:1}
footer{text-align:center;padding:24px;font-size:14px;color:#64748b}
</style>
</head>
<body>
<div class="hero">
  <h1>Get One Licensed Contractor Today</h1>
  <p>Water damage, mold, roofing, or remodel? We match you with one vetted Twin Cities pro. Your phone won’t blow up.</p>
  <p><strong>Exclusive Match · One Contractor Only · No Shared Leads</strong></p>
</div>
<div class="container">
  <div class="steps">
    <div class="step"><h3>1. Tell Us</h3><p>Describe the job and your ZIP.</p></div>
    <div class="step"><h3>2. We Match</h3><p>One verified contractor is selected.</p></div>
    <div class="step"><h3>3. They Call</h3><p>Only one pro contacts you.</p></div>
  </div>
  <div class="card">
    <h2>Request Help</h2>
    <p>Exclusive matching. One contractor only.</p>
    <form method="post" action="/submit">
      <input name="name" placeholder="Full Name" required>
      <input name="phone" placeholder="Phone" required>
      <input name="email" type="email" placeholder="Email" required>
      <input name="zip" placeholder="ZIP Code" required pattern="[0-9]{5}">
      <select name="service_type" required>
        <option value="">Service Needed</option>
        <option>Water Damage / Mold</option>
        <option>Roofing</option>
        <option>Siding</option>
        <option>Windows</option>
        <option>Kitchen / Bath Remodel</option>
        <option>Addition</option>
        <option>Other</option>
      </select>
      <textarea name="details" rows="4" placeholder="What happened? Details of the job..."></textarea>
      <p style="font-size:13px;color:#475569">
        <strong>Consumer Agreement</strong><br>
        By submitting you agree Restoration Contractors MN will match you with one licensed Minnesota contractor.
        We verify Minnesota license only — not insurance. You confirm insurance before work begins.
        No shared leads. Subject to Minnesota law (including Home Solicitation Sales Act).
      </p>
      <button type="submit">Get My Free Match Now</button>
    </form>
  </div>
</div>
<footer>
  <a href="/privacy">Privacy Policy</a> · <a href="/terms">Terms & Conditions</a><br>
  Restoration Contractors MN · Albert R LaMotte dba Restoration Contractors MN
</footer>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form.to_dict()
    data["created_at"] = datetime.utcnow().isoformat()
    with get_db() as db:
        db.execute("""INSERT INTO leads (name,phone,email,zip,service_type,details,created_at)
                      VALUES (:name,:phone,:email,:zip,:service_type,:details,:created_at)""", data)
    return "<h2>Thank You!</h2><p>One contractor will contact you shortly. No shared leads.</p><a href='/'>Back</a>"

@app.route("/privacy")
def privacy():
    return "<h1>Privacy Policy</h1><p>We collect contact and project details solely to match you with one contractor. We do not share leads with multiple contractors.</p><a href='/'>Home</a>"

@app.route("/terms")
def terms():
    return "<h1>Terms</h1><p>Matching service only. We do not perform the work. Governed by Minnesota law.</p><a href='/'>Home</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
