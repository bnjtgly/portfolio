from flask import Flask, render_template, request, redirect
import csv, os, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GMAIL_ADDRESS = os.environ.get('GMAIL_ADDRESS')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/<string:page>")
def pages(page):
    return render_template(page)


def send_email(data):
    email = data['email']
    subject = data['subject']
    message = data['message']

    msg = MIMEMultipart()
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = GMAIL_ADDRESS
    msg['Subject'] = f"Portfolio Contact: {subject}"

    body = f"From: {email}\nSubject: {subject}\n\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, GMAIL_ADDRESS, msg.as_string())


def write_to_csv(data):
    file_exists = os.path.isfile('db.csv')
    with open('db.csv', mode='a') as db:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(db, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if not file_exists:
            csv_writer.writerow(['email', 'subject', 'message'])
            db.write('\n')
        csv_writer.writerow([email, subject, message])


@app.route("/submit_form", methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        try:
            send_email(data)
        except Exception as e:
            print(f"Email failed to send: {e}")
        return redirect('/thankyou.html')
    else:
        return 'Something went wrong.'
