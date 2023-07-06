import sqlite3

# # Connect to the database
# conn = sqlite3.connect('movie.db')
# cursor = conn.cursor()

# # Add the for_kids column
# cursor.execute("ALTER TABLE movies ADD COLUMN feedback_link URL")

# # Commit the changes and close the connection
# conn.commit()
# conn.close()

# Connect to the database
conn = sqlite3.connect('movie.db')
cursor = conn.cursor()

# Create the episodes table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS episodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        series_id INTEGER,
        episode_number INTEGER,
        drive_id TEXT,
        FOREIGN KEY (series_id) REFERENCES series (id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
