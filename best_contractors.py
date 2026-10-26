from flask import Flask, request, redirect, url_for, render_template_string
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me")

CONTRACTOR_SIGNUP = "https://contractors.restorationcontractorsmn.com/signup"
CONTACT_EMAIL = "info@restorationcontractorsmn.com"

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@500;700&family=Inter:wght@400;500;600&display=swap');
:root {
  --primary: #1d4ed8;
  --primary-dark: #1e40af;
  --accent: #d97706;
  --success: #047857;
  --neutral-50: #f8fafc;
  --neutral-100: #f1f5f9;
  --neutral-700: #334155;
  --neutral-900: #0f172a;
  --card: #ffffff;
}
* { box-sizing: border-box; }
body { margin: 0; font-family: Inter, system-ui, sans-serif; background: var(--neutral-50); color: var(--neutral-700); line-height: 1.5; }
.hero {
  background: linear-gradient(160deg, #0f172a 0%, #1e3a8a 55%, #1d4ed8 100%);
  color: white;
  padding: 80px 20px 64px;
  text-align: center;
}
.hero h1 {
  font-family: "DM Sans", sans-serif;
  font-size: clamp(2.2rem, 6vw, 3.6rem);
  font-weight: 700;
  margin: 0 0 16px;
  letter-spacing: -0.02em;
  line-height: 1.1;
}
.hero p { font-size: 1.15rem; max-width: 640px; margin: 0 auto 32px; opacity: 0.95; }
.badge {
  display: inline-block;
  background: rgba(255,255,255,0.15);
  padding: 8px 16px;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 20px;
}
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 0 28px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1.05rem;
  text-decoration: none;
  margin: 6px;
  transition: background .15s;
}
.btn-primary { background: var(--primary); color: white; }
.btn-primary:hover { background: var(--primary-dark); }
.btn-accent { background: var(--accent); color: #0f172a; }
.btn-accent:hover { background: #b45309; color: white; }
.container { max-width: 960px; margin: 0 auto; padding: 0 20px; }
.card {
  background: var(--card);
  border-radius: 16px;
  padding: 32px;
  margin: 28px 0;
  box-shadow: 0 4px 24px rgba(15,23,42,0.06);
  border: 1px solid #e2e8f0;
}
.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-top: 24px;
}
.step { text-align: center; }
.step-num {
  width: 48px; height: 48px;
  background: var(--primary);
  color: white;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.25rem;
  margin-bottom: 12px;
}
h2 { font-family: "DM Sans", sans-serif; color: var(--neutral-900); font-weight: 700; }
label { display: block; font-weight: 500; margin-bottom: 6px; color: var(--neutral-700); }
input, select, textarea {
  width: 100%;
  padding: 14px 16px;
  margin-bottom: 16px;
  border: 1.5px solid #cbd5e1;
  border-radius: 10px;
  font-size: 16px;
  font-family: inherit;
  min-height: 48px;
}
input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(29,78,216,0.15);
}
button[type=submit] {
  background: var(--primary);
  color: white;
  border: none;
  padding: 16px 36px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1.05rem;
  min-height: 48px;
  cursor: pointer;
}
button[type=submit]:hover { background: var(--primary-dark); }
footer { text-align: center; padding: 48px 20px; color: #64748b; font-size: 0.9rem; }
.exclusive-note {
  background: #ecfdf5;
  color: #047857;
  padding: 12px 16px;
  border-radius: 10px;
  font-weight: 500;
  margin: 16px 0;
}
@media (max-width: 640px) {
  .hero { padding: 56px 16px 40px; }
  .card { padding: 24px 16px; }
}
</style>
"""

def send_email(to, subject, body):
    host = os.environ.get("SMTP_HOST")
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASS")
    if not all([host, user, password]):
        print(f"[Email] {subject} -> {to}")
        return
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = user
        msg["To"] = to
        with smtplib.SMTP(host, int(os.environ.get("SMTP_PORT", 587))) as s:
            s.starttls()
            s.login(user, password)
            s.send_message(msg)
    except Exception as e:
        print("Email error:", e)

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Best Contractors Twin Cities — One Pro. No Shared Leads.</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; color: #0f172a; background: #fff; line-height: 1.5; }
.nav { padding: 18px 24px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; }
.nav a { color: #0ea5e9; font-weight: 600; text-decoration: none; }
.nav a:hover { text-decoration: underline; }
.logo { font-weight: 700; font-size: 1.15rem; }
.hero { background: linear-gradient(160deg, #0f172a 0%, #1e3a8a 100%); color: white; padding: 80px 20px 60px; text-align: center; }
.hero h1 { font-size: 2.6rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 12px; line-height: 1.15; }
.hero p { font-size: 1.2rem; opacity: 0.92; max-width: 560px; margin: 0 auto 28px; }
.badges { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; margin-bottom: 28px; }
.badge { background: rgba(255,255,255,0.12); padding: 6px 14px; border-radius: 999px; font-size: 0.85rem; font-weight: 500; }
.cta { display: inline-block; background: #0ea5e9; color: white; padding: 16px 32px; border-radius: 10px; font-weight: 600; text-decoration: none; font-size: 1.05rem; }
.cta:hover { background: #0284c7; }
.section { max-width: 900px; margin: 0 auto; padding: 60px 20px; }
h2 { text-align: center; font-size: 1.8rem; margin-bottom: 8px; }
.sub { text-align: center; color: #64748b; margin-bottom: 32px; }
.steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 24px; }
.step { text-align: center; }
.num { width: 42px; height: 42px; background: #0ea5e9; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; font-weight: 700; }
.form-wrap { background: #f8fafc; padding: 50px 20px; }
.form-card { background: white; border-radius: 16px; padding: 32px; max-width: 480px; margin: 0 auto; box-shadow: 0 8px 30px rgba(0,0,0,0.07); }
label { display: block; font-weight: 500; margin: 14px 0 6px; font-size: 0.95rem; }
input, select, textarea { width: 100%; padding: 13px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 16px; }
button { width: 100%; background: #0ea5e9; color: white; border: none; padding: 16px; border-radius: 8px; font-size: 17px; font-weight: 600; margin-top: 16px; cursor: pointer; }
button:hover { background: #0284c7; }
.agreement { border: 1px solid #e2e8f0; padding: 14px; margin: 14px 0; background: #f8fafc; font-size: 13.5px; border-radius: 8px; }
.note { background: #fef3c7; color: #854d0e; padding: 10px 14px; border-radius: 8px; margin-bottom: 14px; font-weight: 600; font-size: 0.95rem; }
.footer { text-align: center; padding: 30px 20px; color: #64748b; font-size: 0.9rem; }
@media (max-width: 640px) { .hero h1 { font-size: 2rem; } .hero { padding: 60px 16px 40px; } }
</style>
</head>
<body>
<div class="nav">
  <div class="logo">Restoration Contractors MN</div>
  <a href="https://contractors.restorationcontractorsmn.com/signup">Contractor Signup</a>
</div>
<div class="hero">
  <div class="badges">
    <span class="badge">Exclusive Match</span>
    <span class="badge">One Contractor Only</span>
    <span class="badge">No Shared Leads</span>
  </div>
  <h1>Get One Licensed Contractor Today</h1>
  <p>Water damage, mold, roofing, or remodel? We match you with one vetted Twin Cities pro. Your phone won’t blow up.</p>
  <a href="#form" class="cta">Get My Contractor</a>
  <a href="https://contractors.restorationcontractorsmn.com/signup" class="cta" style="background:#d97706;margin-left:8px;">Contractors: Join Here</a>
</div>
<div class="section">
  <h2>How It Works</h2>
  <p class="sub">Simple. Exclusive. Fast.</p>
  <div class="steps">
    <div class="step"><div class="num">1</div><strong>Tell Us</strong><p style="color:#64748b;margin-top:6px;">Describe the job and your ZIP.</p></div>
    <div class="step"><div class="num">2</div><strong>We Match</strong><p style="color:#64748b;margin-top:6px;">One verified contractor is selected.</p></div>
    <div class="step"><div class="num">3</div><strong>They Call</strong><p style="color:#64748b;margin-top:6px;">Only one pro contacts you.</p></div>
  </div>
</div>
<div class="form-wrap" id="form">
  <div class="form-card">
    <h2 style="text-align:left;font-size:1.5rem;margin-bottom:6px;">Request Help</h2>
    <p style="color:#64748b;margin-bottom:12px;">Exclusive matching. One contractor only.</p>
    <div class="note">Your information goes to one contractor only — no shared leads.</div>
    <form method="post" action="/submit">
      <label>Name</label><input name="name" required>
      <label>Phone</label><input name="phone" type="tel" required>
      <label>Email</label><input name="email" type="email" required>
      <label>ZIP Code</label>
      <input name="zip" required pattern="[0-9]{5}" placeholder="55416" title="Enter a 5-digit ZIP code (example: 55416)" maxlength="5" inputmode="numeric">
      <label>Service</label>
      <select name="service" required>
        <option value="">What do you need?</option>
        <optgroup label="Restoration & Emergency">
          <option>Water Damage Restoration</option>
          <option>Mold Inspection & Remediation</option>
          <option>Dry Out / Structural Drying</option>
          <option>Storm Damage Restoration</option>
          <option>Fire & Smoke Cleanup</option>
          <option>Sewage Backup Cleanup</option>
        </optgroup>
        <optgroup label="Exterior & Roofing">
          <option>Roofing</option>
          <option>Siding</option>
          <option>Windows</option>
          <option>Gutters & Downspouts</option>
          <option>Decks & Patios</option>
          <option>Fencing</option>
          <option>Concrete / Driveways / Sidewalks</option>
          <option>Masonry / Brickwork</option>
        </optgroup>
        <optgroup label="Interior Remodel">
          <option>Kitchen Remodel</option>
          <option>Bathroom Remodel</option>
          <option>Basement Remodel / Finish</option>
          <option>Flooring (Hardwood, LVP, Tile, Carpet)</option>
          <option>Painting (Interior / Exterior)</option>
          <option>Drywall & Plaster Repair</option>
          <option>General Remodel / Additions</option>
          <option>Closet Organization / Built-ins</option>
        </optgroup>
        <optgroup label="Systems">
          <option>Plumbing</option>
          <option>Electrical</option>
          <option>HVAC (Heating & Cooling)</option>
          <option>Insulation</option>
          <option>Water Heater Installation / Repair</option>
        </optgroup>
        <optgroup label="Other">
          <option>Handyman</option>
          <option>Tree Removal / Trimming</option>
          <option>Lawn Care / Landscaping</option>
          <option>Snow Removal</option>
          <option>Pressure Washing</option>
          <option>Garage Door Repair / Install</option>
          <option>Other</option>
        </optgroup>
      </select>
      <label>Details</label><textarea name="details" rows="3" placeholder="Briefly describe the job"></textarea>
      <div class="agreement">
        <strong>Consumer Agreement</strong><br>
        By submitting this form you agree:<br>
        - Restoration Contractors MN will match you with one licensed Minnesota contractor<br>
        - We verify the contractor’s Minnesota license only — not insurance<br>
        - You are responsible for confirming the contractor carries insurance before work begins<br>
        - No shared leads — only one contractor will contact you<br>
        - All agreements are subject to Minnesota law (including the Home Solicitation Sales Act)<br>
        <label style="display:block;margin-top:10px;">
          <input type="checkbox" name="agree" required style="width:auto;margin-right:6px;"> I agree to the Consumer Agreement and the <a href="/terms">Terms</a> and <a href="/privacy">Privacy Policy</a>
        </label>
      </div>
      <button type="submit">Get My Free Match Now</button>
    </form>
    <p style="text-align:center;font-size:13px;color:#64748b;margin-top:12px;">No obligation. One contractor. Fast response.</p>
  </div>
</div>
<div class="footer">
  <a href="/privacy">Privacy Policy</a> · <a href="/terms">Terms & Conditions</a><br>
  Restoration Contractors MN · Albert R LaMotte dba Restoration Contractors MN
</div>
</body>
</html>
    """)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.form.to_dict()
    body = f"""New exclusive lead from Restoration Contractors MN

Service: {data.get('service')}
ZIP: {data.get('zip')}
Name: {data.get('name')}
Phone: {data.get('phone')}
Email: {data.get('email')}
Details: {data.get('details')}
"""
    send_email(CONTACT_EMAIL, "New Exclusive Lead — Restoration Contractors MN", body)
    return render_template_string(f"""
    {STYLE}
    <div class="container">
      <div class="card" style="text-align:center;margin-top:40px;">
        <h2>Request Received</h2>
        <p>Thank you, {data.get('name')}. One Minnesota-licensed contractor will contact you shortly. No one else will call.</p>
        <a href="/" class="btn btn-primary">Back to Home</a>
      </div>
    </div>
    """)

@app.route("/privacy")
def privacy():
    return render_template_string(STYLE + """
<div class="container"><div class="card">
  <h1>Privacy Policy</h1>
  <p><strong>Effective Date:</strong> October 26, 2026</p>
  <p>Albert R LaMotte dba Restoration Contractors MN (“we,” “us,” or “our”) operates the websites restorationcontractorsmn.com and contractors.restorationcontractorsmn.com and the exclusive lead-matching service. This Privacy Policy explains how we collect, use, and share information. It is governed by Minnesota law.</p>

  <h2>1. Information We Collect</h2>
  <p><strong>From homeowners:</strong> Name, phone number, email address, ZIP code, service requested, project details, and any other information submitted on the consumer form.</p>
  <p><strong>From contractors:</strong> Company name, contact name, phone number, email address, services offered, service area, and any other information submitted during signup.</p>
  <p><strong>Automatically collected:</strong> IP address, browser type, device information, and pages visited through standard server logs.</p>
  <p><strong>Communications:</strong> Records of emails or text messages related to lead matching or account management.</p>

  <h2>2. How We Use Information</h2>
  <ul>
    <li>To match homeowners with one exclusive contractor.</li>
    <li>To notify contractors of available exclusive leads and to notify homeowners when a contractor accepts their lead.</li>
    <li>To manage contractor accounts and process lead acceptance.</li>
    <li>To send transactional emails and SMS messages related to lead matching.</li>
    <li>To improve the sites, prevent fraud, and comply with Minnesota law.</li>
  </ul>

  <h2>3. SMS and Email Communications</h2>
  <p>By providing your phone number and checking the consent box (or submitting the form), you expressly consent to receive text messages and emails from us related to exclusive lead matching. Message and data rates may apply. Reply STOP to any SMS to opt out. You may unsubscribe from emails using the link in the message or by contacting us. Consent is not a condition of using the matching service.</p>

  <h2>4. Sharing of Information</h2>
  <p>Homeowner contact information is shared <strong>only</strong> with the single contractor who accepts the exclusive lead. Contractor contact information is shared with the homeowner only after the contractor accepts the lead. We do not sell, rent, or share the same lead with multiple contractors. We may share information with service providers (hosting, email, SMS) solely to operate the service, and as required by law.</p>

  <h2>5. Data Retention</h2>
  <p>We retain information as long as needed to provide the service, resolve disputes, and comply with legal obligations under Minnesota law.</p>

  <h2>6. Your Rights</h2>
  <p>Minnesota residents may request access to, correction of, or deletion of their personal information by contacting us. We will respond in accordance with applicable Minnesota law.</p>

  <h2>7. Contact</h2>
  <p>Albert R LaMotte dba Restoration Contractors MN<br>
  Email: info@restorationcontractorsmn.com</p>

  <h2>8. Changes</h2>
  <p>We may update this Privacy Policy. The updated version will be posted on the sites with a new effective date.</p>

  <p><a href="/">← Home</a></p>
</div></div>

    """)

@app.route("/terms")
def terms():
    return render_template_string(STYLE + """
<div class="container"><div class="card">
  <h1>Terms & Conditions</h1>
  <p><strong>Effective Date:</strong> October 26, 2026</p>
  <p>These Terms & Conditions (“Terms”) govern your use of the websites restorationcontractorsmn.com and contractors.restorationcontractorsmn.com and the exclusive lead-matching service operated by Albert R LaMotte dba Restoration Contractors MN (“we,” “us,” or “our”).</p>

  <h2>1. Exclusive Leads Only</h2>
  <p>All leads provided through this service are exclusive. A lead is offered to only one contractor at a time. We do not sell or share the same lead with multiple contractors. Contact information remains hidden until the contractor accepts the lead.</p>

  <h2>2. Homeowner Terms</h2>
  <p>By submitting a lead form, you authorize us to share your contact information and project details with one contractor who accepts the exclusive lead. You agree that the contractor is an independent business, not our employee or agent. You acknowledge that the Minnesota Home Solicitation Sales Act (Minn. Stat. §§ 325G.06–325G.11) and other applicable Minnesota consumer protection laws may apply to any in-home solicitation or contract with the contractor. You may cancel certain home solicitation contracts within the time periods required by Minnesota law.</p>

  <h2>3. Contractor Terms</h2>
  <p>Contractors must provide accurate information. Acceptance of a lead constitutes an agreement to contact the homeowner promptly. Contractors may accept or reject a lead. Unaccepted leads expire after 24 hours. Contractors are independent businesses. We do not guarantee the quality, outcome, or legality of any work performed.</p>

  <h2>4. Minnesota Law</h2>
  <p>These Terms and all agreements related to the service are governed by the laws of the State of Minnesota, without regard to conflict-of-law principles. Any disputes shall be resolved in the state or federal courts located in Minnesota. The Minnesota Home Solicitation Sales Act and other applicable Minnesota statutes apply where relevant.</p>

  <h2>5. No Shared Leads</h2>
  <p>We expressly do not operate a shared-lead model. Each lead is exclusive to one contractor.</p>

  <h2>6. Limitation of Liability</h2>
  <p>To the fullest extent permitted by Minnesota law, we are not liable for the acts, omissions, quality of work, or contractual disputes between homeowners and contractors. Our role is limited to exclusive lead matching.</p>

  <h2>7. SMS and Email Consent</h2>
  <p>By providing a phone number and submitting a form, you consent to receive transactional SMS and email messages related to lead matching. You may opt out of SMS by replying STOP.</p>

  <h2>8. Changes</h2>
  <p>We may update these Terms. Continued use of the sites after changes constitutes acceptance of the updated Terms.</p>

  <h2>9. Contact</h2>
  <p>Albert R LaMotte dba Restoration Contractors MN<br>
  Email: info@restorationcontractorsmn.com</p>

  <p><a href="/">← Home</a></p>
</div></div>

    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
