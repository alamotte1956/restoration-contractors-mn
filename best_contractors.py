from flask import Flask, request, session, redirect, url_for, render_template_string
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")
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
                name TEXT,
                phone TEXT,
                email TEXT,
                zip TEXT,
                service_type TEXT,
                details TEXT,
                urgency TEXT,
                property_type TEXT,
                created_at TEXT,
                status TEXT DEFAULT 'new'
            );
        """)

init_db()

HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Restoration Contractors MN — One Pro. No Shared Leads.</title>
<style>
body{font-family:system-ui,-apple-system,sans-serif;margin:0;background:#f8fafc;color:#1e293b;line-height:1.5}
.hero{background:linear-gradient(135deg,#0f172a,#1e40af);color:#fff;padding:60px 20px;text-align:center}
.container{max-width:720px;margin:32px auto;padding:0 20px}
.card{background:#fff;border-radius:12px;padding:28px;box-shadow:0 4px 20px rgba(0,0,0,.08)}
input,select,textarea{width:100%;padding:12px;margin:8px 0 16px;border:1px solid #cbd5e1;border-radius:8px;box-sizing:border-box;font-size:16px}
button{width:100%;background:#0ea5e9;color:#fff;border:none;padding:16px;border-radius:8px;font-size:18px;cursor:pointer;font-weight:600}
.steps{display:flex;gap:12px;margin:28px 0;text-align:center;flex-wrap:wrap}
.step{flex:1;min-width:160px;background:#fff;padding:16px;border-radius:8px}
footer{text-align:center;padding:20px;font-size:14px;color:#64748b}
a{color:#0ea5e9}
</style>
</head>
<body>
<div class="hero">
  <h1>Get One Licensed Contractor Today</h1>
  <p>Water damage, mold, roofing, siding, windows, or remodel? We match you with one vetted Twin Cities pro.</p>
  <p><strong>Exclusive Match · One Contractor Only · No Shared Leads · Your Phone Won’t Blow Up</strong></p>
</div>
<div class="container">
  <div class="steps">
    <div class="step"><h3>1. Tell Us</h3><p>Describe the job and your ZIP.</p></div>
    <div class="step"><h3>2. We Match</h3><p>One verified contractor is selected.</p></div>
    <div class="step"><h3>3. They Call</h3><p>Only one pro contacts you.</p></div>
  </div>
  <div class="card">
    <h2>Request Help</h2>
    <p>Exclusive matching. One contractor only. No shared leads.</p>
    <form method="post" action="/submit">
      <label>Name *</label><input name="name" required>
      <label>Phone *</label><input name="phone" type="tel" required placeholder="(612) 555-1234">
      <label>Email *</label><input name="email" type="email" required>
      <label>ZIP Code *</label><input name="zip" required pattern="[0-9]{5}" placeholder="55406">
      <label>Service Needed *</label>
      <select name="service_type" required>
        <option value="">Select service</option>
        <option>Water Damage / Mold</option>
        <option>Roofing</option>
        <option>Siding</option>
        <option>Windows</option>
        <option>Kitchen / Bath Remodel</option>
        <option>Addition</option>
        <option>Other</option>
      </select>
      <label>Details</label>
      <textarea name="details" rows="4" placeholder="What happened? Where is the damage? How urgent?"></textarea>
      <p style="font-size:13px;color:#475569;background:#f1f5f9;padding:12px;border-radius:8px">
        <strong>Consumer Agreement (Minnesota Law)</strong><br>
        By submitting you agree that Restoration Contractors MN (Albert R LaMotte dba) will match you with one licensed Minnesota contractor. We verify Minnesota license only — not insurance. You are responsible for confirming insurance and workers’ compensation before work begins. No shared leads. This service is subject to Minnesota law, including the Home Solicitation Sales Act. You may cancel within the statutory period where applicable.
      </p>
      <button type="submit">Get My Free Match Now</button>
    </form>
  </div>
</div>
<footer>
  <a href="/privacy">Privacy Policy</a> · <a href="/terms">Terms & Conditions</a><br>
  Restoration Contractors MN · Albert R LaMotte dba Restoration Contractors MN<br>
  Exclusive leads only. No shared leads.
</footer>
</body>
</html>
"""

@app.route("/")
def home():
    return HOME_HTML

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form.to_dict()
    data["created_at"] = datetime.utcnow().isoformat()
    with get_db() as db:
        db.execute("""
            INSERT INTO leads (name, phone, email, zip, service_type, details, created_at)
            VALUES (:name, :phone, :email, :zip, :service_type, :details, :created_at)
        """, data)
    return """
    <h2>Thank You!</h2>
    <p>One licensed contractor will contact you shortly. No shared leads — your phone will not blow up.</p>
    <p><a href="/">Back to home</a></p>
    """

@app.route("/privacy")
def privacy():
    return """
    <h1>Privacy Policy</h1>
    <p>We collect your name, phone, email, ZIP, and project details solely to match you with one contractor. We do not sell or share your information with multiple contractors. Data is retained only as long as needed for matching and legal compliance. Subject to Minnesota privacy and consumer protection laws.</p>
    <p><a href="/">Home</a></p>
    """

@app.route("/terms")
def terms():
    return """
    <h1>Terms & Conditions</h1>
    <p>This is a matching service only. Restoration Contractors MN does not perform construction or restoration work. All work is performed by independent licensed contractors. You must verify insurance. Governed by Minnesota law. No shared leads.</p>
    <p><a href="/">Home</a></p>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
