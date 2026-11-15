import sqlite3

conn = None
cursor = None

def connect():
    global conn, cursor
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

def close():
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def create_tables():
    connect()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        photo TEXT,
        login TEXT,
        password TEXT,
        description TEXT,
        description_short TEXT
    )
    ''')
    cursor.execute('''
    create table if not exists categories (
        category_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    ''')
    cursor.execute('''
    create table if not exists posts (
    post_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        text TEXT,
        datetime TEXT,
        FOREIGN KEY (category_id) REFERENCES categories (category_id)
    )
    ''')
    conn.commit()
    close()

def add_user(name, photo, login, password, description, description_short):
    connect()
    cursor.execute("""
                    INSERT INTO users (name,photo,login,password,description,description_short)
                    VALUES (?,?,?,?,?,?,?)""",
                   (name, photo, login, password, description, description_short))
    conn.commit()
    close()

def get_user():
    connect()
    cursor.execute("SELECT * FROM users")
    user = cursor.fetchone()
    close()
    return user
def add_category(name):
    connect()
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    close()

def add_post(category_id,text,datetime):
    connect()
    cursor.execute('''INSERT INTO posts (category_id,text,datetime) 
                   VALUES (?,?,?)
                   ''',
                   (category_id,text,datetime))
    conn.commit()
    close()


def get_categories():
    connect()
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    close()
    return categories

def get_posts(category_id):
    connect()
    cursor.execute(
        """
        SELECT * FROM posts, categories 
        WHERE posts.category_id = categories.category_id
        and posts.category_id = ?
        """, (category_id,)
    )
    posts = cursor.fetchall()
    close()
    return posts

def show_posts(category_id):
    posts = get_posts(category_id)

    for post in posts:
        print("Текст:", post["text"])
        print("Категорія:", post["name"])
        print('-'*50)


def get_category_by_name(category_name):
    connect()
    cursor.execute(
        '''SELECT * FROM categories WHERE name = ?''',
        [category_name]
    )
    category = cursor.fetchone()
    close()

    return category


def get_post(post_id):
    connect()
    post = cursor.execute("""
            SELECT posts.*, categories.name AS category_name
            FROM posts
            JOIN categories ON categories.category_id = posts.category_id
            WHERE posts.post_id = ?
        """, (post_id,)).fetchone()
    close()
    return post
