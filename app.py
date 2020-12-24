import sqlite3
import time
from hashlib import md5
from PIL import Image
from flask import Flask, render_template, request, url_for, flash, redirect, g, abort, send_from_directory
from werkzeug.utils import secure_filename
from config import *


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'Bastien_secret_key'

def check_extension(extension):
    """
    Make sure extension is in the ALLOWED_EXTENSIONS set
    """
    return extension in app.config['ALLOWED_EXTENSIONS']

# def read(fname):
#     """
#     Utility function to read the README file.
#     Used for the long_description.  It's nice, because now 1) we have a top level
#     README file and 2) it's easier to type in the README file than to put a raw
#     string in below ...
#     """
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()

# def connect_db():
#     """ Connect to the SQLite database.
#     """
#     query = open(app.config['SCHEMA'], 'r').read()
#     conn = sqlite3.connect(app.config['DATABASE'])
#     cursor = conn.cursor()
#     cursor.executescript(query)
#     conn.commit()
#     cursor.close()
#     return sqlite3.connect(app.config['DATABASE'])

# def connect_db():
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     return conn

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = connect_db()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_last_pics():
    """ Return a list of the last 25 uploaded images
    """
    db = connect_db()
    cur = db.execute('select filename from pics order by created_on desc limit 25')
    filenames = [row[0] for row in cur.fetchall()]
    return filenames


def add_pic(filename):
    """ Insert filename into database
    """
    g.db.execute('insert into pics (filename) values (?)', [filename])
    g.db.commit()

def gen_thumbnail(filename):
    """ Generate thumbnail image
    """
    height = width = 200
    original = Image.open(os.path.join(app.config['UPLOAD_DIR'], filename))
    thumbnail = original.resize((width, height), Image.ANTIALIAS)
    thumbnail.save(os.path.join(app.config['UPLOAD_DIR'], 'thumb_'+filename))





@app.route('/', methods=['GET', 'POST'])
def index():
    conn = connect_db()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    """ Default route.
    """
    # if request.method == 'POST':
    #     image_file = request.files['file']
    #     try:
    #         extension = image_file.filename.rsplit('.', 1)[1].lower()
    #     except IndexError as err:
    #         app.logger.info(err.message)
    #         abort(404)
    #     if image_file and check_extension(extension):
    #         # Salt and hash the file contents
    #         filename = md5(image_file.read() +
    #                        str(round(time.time() * 1000))
    #                       ).hexdigest() + '.' + extension
    #         image_file.seek(0) # Move cursor back to beginning so we can write to disk
    #         image_file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
    #         add_pic(filename)
    #         gen_thumbnail(filename)
    #         return redirect(url_for('show_pic', filename=filename))
    #     else: # Bad file extension
    #         abort(404)
    # else:
    return render_template('index.html', posts=posts)

# @app.route('/')
# def index():
#     conn = connect_db()
#     posts = conn.execute('SELECT * FROM posts').fetchall()
#     conn.close()
#     return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = connect_db()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = connect_db()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = connect_db()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


@app.route('/pics/<filename>')
def return_pic(filename):
    """ Show just the image specified.
    """
    return send_from_directory(app.config['UPLOAD_DIR'], secure_filename(filename))
