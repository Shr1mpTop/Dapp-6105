from flask import Flask, render_template, request
import sqlite3
import datetime

# Register datetime adapter and converter for sqlite3
sqlite3.register_adapter(datetime.datetime, lambda dt: dt.isoformat())
sqlite3.register_converter("timestamp", lambda s: datetime.datetime.fromisoformat(s))

app = Flask(__name__)
@app.route("/", methods=["GET","POST"])
def index():
    global flag
    flag = 1
    return(render_template("index.html"))

@app.route("/main", methods=["GET","POST"])
def main():
    global flag
    if flag == 1:
        name = request.form.get("q")
        if name:
            t = datetime.datetime.now()
            conn = sqlite3.connect('user.db')
            c = conn.cursor()
            c.execute('INSERT INTO user (name,timestamp) VALUES(?,?)',(name,t))
            conn.commit()
            c.close()
            conn.close()
            flag = 0
    return(render_template("main.html"))

@app.route("/paynow", methods=["GET","POST"])
def paynow():
    return(render_template("paynow.html"))

@app.route("/deposit", methods=["GET","POST"])
def deposit():
    return(render_template("deposit.html"))

@app.route("/userlog", methods=["GET","POST"])
def userlog():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('''select * from user''')
    r=""
    for row in c:
        r = r + str(row) + "<br>"
    c.close()
    conn.close()
    return(render_template("userlog.html",r=r))

@app.route("/deleteuserlog", methods=["GET","POST"])
def deleteuserlog():
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute('DELETE FROM user')
        conn.commit()
        c.close()
        conn.close()
        return(render_template("deleteuserlog.html"))

if __name__ == "__main__":
    app.run()