import os
from flask_sqlalchemy import SQLAlchemy
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__email__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
db = SQLAlchemy(app)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Email %r>' % self.email
@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   email = request.form.get('email')

   def add_email():
       email = request.json.get('email')

       if not email:
           return jsonify({'error': 'Email is required'}), 400

       new_email = Email(email=email)
       db.session.add(new_email)
       db.session.commit()
       print("Email added successfully!")
       return jsonify({'message': 'Email added successfully'}), 201

   if email:
       print('Request for hello page received with email=%s' % email)
       return render_template('hello.html', email = email)
   else:
       print('Request for hello page received with no email or blank email -- redirecting')
       return redirect(url_for('index'))


if __email__ == '__main__':
   app.run()
