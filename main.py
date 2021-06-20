from flask import Flask, request, jsonify
import sqlite3




def init_db():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
	    id                 INTEGER PRIMARY KEY,
	    REALTIME_TIMESTAMP TEXT NOT NULL,
	    HOSTNAME           TEXT NOT NULL,
	    SYSLOG_FACILITY    TEXT NOT NULL,
        PRIORITY           TEXT NOT NULL,
        MESSAGE            TEXT NOT NULL
    );
    """)
    con.commit()
    cur.close()
    

def insert(data) -> int:
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    try:
        cur.execute("""
   INSERT INTO events (REALTIME_TIMESTAMP, HOSTNAME, SYSLOG_FACILITY, PRIORITY, MESSAGE) VALUES (?, ?, ?, ?, ?)
        """, (data["__REALTIME_TIMESTAMP"], data["_HOSTNAME"], data["SYSLOG_FACILITY"], data["PRIORITY"], data["MESSAGE"]))
        con.commit()
        cur.close()
        return 200
    except KeyError:
        return 400

 
app = Flask(__name__)


@app.route('/', methods=['POST'])
def main_handler():
    data = request.get_json()
    code = insert(data)
    return jsonify({"status": "OK" if code == 200 else "BAD REQUEST"}), code


if __name__ == '__main__':
    init_db()
    app.run()