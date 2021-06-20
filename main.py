from flask import Flask, request, jsonify
import sqlite3




def init_db():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS errors (
	    id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
	    is_admin INTEGER NOT NULL,
	    date TEXT NOT NULL,
	    time TEXT NOT NULL,
        error_text TEXT NOT NULL
    );
    """)
    con.commit()
    cur.close()
    

def insert(data) -> int:
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    try:
        cur.execute("""
   INSERT INTO errors (is_admin, date, time, name, error_text) VALUES (?, ?, ?, ?, ?)
        """, (data["is_admin"], data["date"], data["time"], data["name"], data["error_text"]))
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