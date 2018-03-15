from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

from dbconnect import connect
from MySQLdb import escape_string

from dotmap import DotMap

from passlib.hash import sha256_crypt as sha256

from functools import wraps

app = Flask(__name__)
CORS(app)

dict_c, c, conn = None, None, None

def db(f):
    @wraps(f)
    def wrap(*a, **kw):
        global dict_c, c, conn

        c, dict_c, conn = connect()
        rv = f(*a, **kw)
        conn.close()
        return rv
    
    return wrap

def es(s):
    return escape_string(s).decode('utf-8')

@app.route('/')
def index():
    return "<h1>We're still developing</h1>"

@app.route('/login', methods=["POST"])
@db
def login():
    uname = request.form['uname']
    passwd = request.form['passwd']

    x = dict_c.execute('select passwd from users where email = "{0}" or uname = "{0}"'.format(
        es(uname)
    ))

    if int(x) == 0:
        return jsonify(code="2", error="No such email or username")
    
    a = dict_c.fetchone()
    print(a)

    fetched_info = DotMap(a)

    if not sha256.verify(passwd, fetched_info.passwd):
        return jsonify(code='3', error="Invalid password")
    
    return jsonify(code="1")

@app.route('/register', methods=["POST"])
@db
def register():
    uname = request.form['uname']
    email = request.form['email']
    passwd = request.form['passwd']

    return jsonify(code="1")
    

if __name__ == "__main__":
    app.run(debug=True, port=8000)
