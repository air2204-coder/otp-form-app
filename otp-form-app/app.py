from flask import Flask, request, render_template, session
import random
import requests
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

FAST2SMS_API_KEY = os.environ.get("FAST2SMS_API_KEY")

def send_otp(mobile, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    params = {
        "authorization": FAST2SMS_API_KEY,
        "route": "otp",
        "variables_values": otp,
        "flash": "0",
        "numbers": mobile,
    }
    requests.get(url, params=params)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/send_otp', methods=['POST'])
def send():
    mobile = request.form['mobile']
    otp = str(random.randint(1000, 9999))

    session['otp'] = otp
    session['mobile'] = mobile

    send_otp(mobile, otp)

    return render_template("verify.html")

@app.route('/verify', methods=['POST'])
def verify():
    user_otp = request.form['otp']

    if user_otp == session.get('otp'):
        return render_template("form.html")
    else:
        return "Invalid OTP"

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    mobile = session.get('mobile')

    form_url = "https://docs.google.com/forms/d/e/YOUR_FORM_ID/formResponse"

    data = {
        "entry.123456": name,
        "entry.654321": mobile
    }

    requests.post(form_url, data=data)

    return "Form submitted successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
