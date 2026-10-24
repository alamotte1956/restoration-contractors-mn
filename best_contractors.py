from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

STYLE = """
<style>
:root { --navy:#0b1f3a; --blue:#0ea5e9; --green:#059669; --bg:#f8fafc; }
* { box-sizing:border-box; }
body { margin:0; font-family:system-ui,-apple-system,sans-serif; background:var(--bg); color:#1e293b; }
.header { background:var(--navy); color:white; padding:20px; text-align:center; }
.hero { background:linear-gradient(135deg,#0b1f3a,#1e40af); color:white; text-align:center; padding:60px 20px; }
.hero h1 { font-size:2.4rem; margin:12px 0; }
.container { max-width:680px; margin:0 auto; padding:28px 20px; }
.card { background:white; border-radius:16px; padding:32px; box-shadow:0 8px 30px rgba(0,0,0,.08); }
.badge { background:#dbeafe; color:#1e40af; padding:6px 14px; border-radius:999px; font-size:.85rem; font-weight:600; }
.btn { background:var(--blue); color:white; border:none; padding:16px; width:100%; border-radius:12px; font-size:1.1rem; font-weight:600; cursor:pointer; }
input,select,textarea { width:100%; padding:14px; margin:8px 0 16px; border:1px solid #e2e8f0; border-radius:10px; font-size:1rem; }
.steps { display:grid; gap:16px; margin:24px 0; }
.step { background:white; padding:16px; border-radius:12px; }
</style>
"""

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        return render_template_string(f"""
        {STYLE}
        <div class="header"><h1>Request Received</h1></div>
        <div class="container"><div class="card" style="text-align:center;">
          <h2>You’re matched</h2>
          <p>One licensed Minnesota contractor will contact you shortly. Your information was not shared with anyone else.</p>
        </div></div>
        """)

    return render_template_string(f"""
    {STYLE}
    <div class="hero">
      <div class="badge">EXCLUSIVE MATCH • ONE CONTRACTOR ONLY</div>
      <h1>Get One Licensed Contractor Today</h1>
      <p>Water damage, mold, roofing, siding, windows, or remodel.<br>One vetted Twin Cities pro. Your phone will not blow up with calls.</p>
    </div>
    <div class="container">
      <div class="steps">
        <div class="step"><strong>1. Tell Us</strong> — Describe the job and your ZIP.</div>
        <div class="step"><strong>2. We Match</strong> — One verified Minnesota contractor is selected.</div>
        <div class="step"><strong>3. They Call</strong> — Only one pro contacts you.</div>
      </div>
      <div class="card">
        <h2>Request Your Exclusive Match</h2>
        <form method="post">
          <input name="name" placeholder="Your Name" required>
          <input name="phone" placeholder="Phone" required>
          <input name="email" type="email" placeholder="Email" required>
          <input name="zip" placeholder="ZIP Code" required>
          <select name="service" required>
            <option value="">Service Needed</option>
            <option>Water Damage / Restoration</option>
            <option>Mold</option>
            <option>Roofing</option>
            <option>Siding</option>
            <option>Windows</option>
            <option>Remodel</option>
          </select>
          <textarea name="details" rows="4" placeholder="Describe the job"></textarea>
          <div style="background:#f1f5f9;padding:14px;border-radius:8px;font-size:.9rem;margin:12px 0;">
            <strong>Consumer Agreement</strong><br>
            By submitting you agree that Restoration Contractors MN (Albert R. LaMotte dba) will match you with one licensed Minnesota contractor. We verify license status only (not insurance). No shared leads. Subject to Minnesota law, including the Home Solicitation Sales Act.
          </div>
          <label style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">
            <input type="checkbox" required style="width:auto;"> I agree to the Consumer Agreement
          </label>
          <button class="btn" type="submit">Get My Free Exclusive Match</button>
        </form>
      </div>
    </div>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
