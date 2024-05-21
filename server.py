from flask import Flask, render_template, request, redirect
import csv, os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/<string:page>")
def pages(page):
    return render_template(page)


def write_to_csv(data):
    file_exists = os.path.isfile('db.csv')
    with open('db.csv', mode='a') as db:
        email = data['email']
        subject = data['subject']
        message = data['subject']
        csv_writer = csv.writer(db, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if not file_exists:  # If file is empty, write header and then data
            csv_writer.writerow(['email', 'subject', 'message'])
            db.write('\n')  # Add a newline after the header
        csv_writer.writerow([email, subject, message])


@app.route("/submit_form", methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/thankyou.html')
    else:
        return 'Something went wrong.'
