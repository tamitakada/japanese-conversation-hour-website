from flask import Flask, render_template, request, abort
from flask_mail import Mail, Message

from dotenv import load_dotenv

import parse
import os


load_dotenv('.env')

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ['EMAIL']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


@app.route("/", methods=["GET", "POST"])
def get_home():
    feature = parse.parse_newsletter("03-12-24")
    all_newsletters = [
        "11-03-23",
        "11-10-23",
        "11-17-23",
        "11-24-23",
        "12-01-23",
        "02-06-24",
        "02-13-24",
        "02-20-24",
        "02-27-24",
        "03-05-24",
        "03-12-24"
    ]
    if request.method == "POST":
        email = request.form["email"]
        message = request.form["message"]
        msg = Message(
            '[和会話教室] New Message from Website Contact Form',
            sender=('和会話教室', os.environ['EMAIL']),
            recipients=[os.environ['EMAIL']]
        )
        msg.body = f"From {email}\nMessage: {message}"
        mail.send(msg)
    return render_template("base.html", feature=feature, newsletters=all_newsletters, initial_selection=all_newsletters[-1])


@app.route("/<date>")
def get_newsletter(date):
    return parse.parse_newsletter(date)


if __name__ == "__main__":
    app.debug = True
    app.run(port=8000)
