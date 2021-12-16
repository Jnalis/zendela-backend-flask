from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jnalis@localhost/simple-formm-4887'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)


class simpleForm(db.Model):
    fname = db.Column(db.Text)
    mname = db.Column(db.Text)
    lname = db.Column(db.Text)
    number = db.Column(db.Text)
    email = db.Column(db.Text, unique=True, primary_key=True)
    address = db.Column(db.Text)

    def __init__(self, fname, mname, lname, number, email, address):
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.number = number
        self.email = email
        self.address = address


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        number = request.form['number']
        email = request.form['email']
        address = request.form['address']
        insert = simpleForm(fname, mname, lname, number, email, address)
        db.session.add(insert)
        db.session.commit()
        msg = 'Successfully registered'
        return render_template('index.html', msg=msg)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    db.create_all()
    app.run()
