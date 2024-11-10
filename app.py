import sqlite3
from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def store_max_human_count(max_count):
    conn = sqlite3.connect('human_detection.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO total_count (total_count, timestamp)
        VALUES (?, datetime('now'))
    """, (max_count,))
    conn.commit()
    conn.close()

def get_recent_total_count():
    conn = sqlite3.connect('human_detection.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT total_count, timestamp FROM total_count
        ORDER BY timestamp DESC LIMIT 1
    ''')
    recent_total_count = cursor.fetchone()

    cursor.execute('''
        SELECT count, timestamp FROM human_count
        ORDER BY timestamp DESC LIMIT 10
    ''')
    data = cursor.fetchall()

    conn.close()
    return recent_total_count, data

@app.route('/api/headcount')
def headcount_api():
    recent_total_count, data = get_recent_total_count()

    if recent_total_count:
        total_count = recent_total_count[0] if recent_total_count[0] is not None else 0
        total_timestamp = recent_total_count[1] if recent_total_count[1] is not None else 'N/A'
    else:
        total_count = 0
        total_timestamp = 'No data'

    response_data = {
        'total_recent_count': total_count,
        'recent_total_timestamp': total_timestamp,
        'data': [{'count': row[0] or 'N/A', 'timestamp': row[1] or 'N/A'} for row in data]
    }

    return jsonify(response_data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
