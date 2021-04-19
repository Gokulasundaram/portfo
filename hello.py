"""
A first simple Cloud Foundry Flask app

Author: Ian Huston
License: See LICENSE.txt

"""
import csv

from flask import Flask, render_template, url_for, request, redirect
import os
from os import environ

app = Flask(__name__)


@app.route('/')
# @app.route('/home')
def home():
    """Renders the home page."""
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    """Renders the html_page page."""
    return render_template(page_name)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect("thankyou.html")
    else:
        return "Form has not been Submitted :("


def write_to_data(data):
    with open("Database.txt", mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{email}, {subject}, {message}')


def write_to_csv(data):
    with open("Database.csv", mode='a') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        csv_writer.writerow([email, subject, message])


if __name__ == '__main__':
    if str(environ.get('VCAP_APPLICATION')) == 'None':
        HOST = environ.get('SERVER_HOST', 'localhost')
        try:
            PORT = int(environ.get('SERVER_PORT', '5555'))
        except ValueError:
            PORT = 5555
        app.run(HOST, PORT, debug=True)
    else:
        port = os.getenv('VCAP_APP_PORT', '8080')
        app.run(host='127.0.0.1', port=int(port), debug=True)
