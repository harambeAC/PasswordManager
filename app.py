from flask import Flask, render_template
import pymongo
import sys
from forms import Form

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

passwords = []

def add_password(col, site, pswd):
    dict = { "website": site, "password": pswd}
    passwords.append(dict)
    x = col.insert_one(dict)

@app.route('/',  methods=['GET', 'POST'])
def manager():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["mongoDatabase"]
    col = db["passwords"]

    passwords = []



    f = Form()
    if f.validate_on_submit():
        print(f.password.data, file=sys.stderr)
        add_password(col ,f.website.data,str(f.password.data))

    for x in col.find():
        passwords.append(x)
        
    return render_template("Manager.html", passwords = passwords, forms=f)

if __name__ == '__main__':
    app.run()
