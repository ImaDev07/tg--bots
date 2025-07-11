import sqlite3


def create_data(user_id, date, time, people, place):
    with sqlite3.connect('ansar.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                time TEXT,
                people INTEGER,
                place TEXT
            )
        ''')
        cursor.execute('''
            INSERT INTO book (user_id, date, time, people, place)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, date, time, people, place))
        conn.commit()


def search_user(user_id):
    with sqlite3.connect('ansar.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM book WHERE user_id = ?', (user_id,))
        return cursor.fetchall()
