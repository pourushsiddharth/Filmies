import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('movie.db')

# Create a cursor object to execute SQL statements
cursor = conn.cursor()

# Create the movies table with the views column
cursor.execute('''
    CREATE TABLE movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        description2 TEXT,
        drive_id TEXT,
        release_date TEXT,
        director TEXT,
        genre TEXT,
        watch_url TEXT,
        poster_url TEXT,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        movie_audio TEXT,
        movie_size FLOAT,
        likes INTEGER,
        dislikes INTEGER,
        unique_key TEXT,
        logo_url TEXT,
        thumbnail_url TEXT,
        views INTEGER DEFAULT 0
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
