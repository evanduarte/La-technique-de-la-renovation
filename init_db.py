import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content, filename) VALUES (?, ?, ?)",
            ('Cloture', 'Content for the first post', 'C:\\Users\\Megaport\\Desktop\HUGUES SITE\\flask_blog\\static\\photo LTR\\cloture.jpg')
            )

cur.execute("INSERT INTO posts (title, content,filename) VALUES (?, ?, ?)",
            ('Baignoire', 'Content for the second post', 'C:\\Users\\Megaport\\Desktop\HUGUES SITE\\flask_blog\\static\\photo LTR\\baignoire.jpg')
            )

connection.commit()
connection.close()
