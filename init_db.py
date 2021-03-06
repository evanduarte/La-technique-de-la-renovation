import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content, filename) VALUES (?, ?, ?)",
            ('Cloture', 'Content for the first post', '/static/photo LTR/cloture.jpg')
            )

cur.execute("INSERT INTO posts (title, content ,filename) VALUES (?, ?, ?)",
            ('Baignoire', 'Content for the second post', '/static/photo LTR/baignoire.jpg')
            )

connection.commit()
connection.close()
