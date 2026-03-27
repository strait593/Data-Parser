import sqlite3
import json

conn = sqlite3.connect("gathered.db")

conn.row_factory = sqlite3.Row
cur = conn.cursor()

def create_quotes():

    cur.execute("SELECT * FROM quotes")
    rows = [dict(row) for row in cur.fetchall()]

    with open("quotes.json", 'w', encoding='utf-8') as file:
        json.dump(rows, file, ensure_ascii=False, indent=4)

    return f"Created a seperate file for quotes"

def create_authors():
    cur.execute("SELECT * FROM Authors")
    rows = [dict(row) for row in cur.fetchall()]

    with open("authors.json", 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=4)

    return f"Created a seperate file for authors"