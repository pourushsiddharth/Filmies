import sqlite3

# Connect to the database
conn = sqlite3.connect('movie.db')
c = conn.cursor()

# Create the "series" table
c.execute('''
    CREATE TABLE IF NOT EXISTS series (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        poster_url TEXT,
        logo_url TEXT,
        genre TEXT,
        ott_platform TEXT,
        trailer_id TEXT,
        for_kids INTEGER,
        total_seasons INTEGER DEFAULT 0
    )
''')

# Create the "seasons" table
c.execute('''
    CREATE TABLE IF NOT EXISTS seasons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        series_id INTEGER,
        poster_url TEXT,
        FOREIGN KEY (series_id) REFERENCES series(id)
    )
''')

# Create the "episodes" table
c.execute('''
    CREATE TABLE IF NOT EXISTS episodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        season_id INTEGER,
        drive_id TEXT,
        FOREIGN KEY (season_id) REFERENCES seasons(id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
