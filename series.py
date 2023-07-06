# import sqlite3

# # Connect to the database
# conn = sqlite3.connect('movie.db')
# cursor = conn.cursor()

# # Add the new column 'poster_url' to the 'series' table
# cursor.execute('ALTER TABLE series ADD COLUMN total_episode INTEGER')

# # Commit the changes and close the connection
# conn.commit()
# conn.close()

# import sqlite3

# def create_series_table():
#     # Connect to the SQLite database
#     conn = sqlite3.connect("movie.db")
#     cursor = conn.cursor()

#     # Create the series table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS series (
#             id INTEGER PRIMARY KEY,
#             name TEXT,
#             description TEXT,
#             genre TEXT,
#             drive_id TEXT,
#             trailer_id TEXT,
#             ott_platform TEXT,
#             for_kids INTEGER,
#             num_episodes INTEGER
#         )
#     ''')

#     # Commit the changes and close the connection
#     conn.commit()
#     conn.close()

import sqlite3

def create_episodes_table():
    # Connect to the SQLite database
    conn = sqlite3.connect("movie.db")
    cursor = conn.cursor()

    # Create the episodes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS episodes (
            id INTEGER PRIMARY KEY,
            series_id INTEGER,
            episode_number INTEGER,
            drive_id TEXT,
            FOREIGN KEY (series_id) REFERENCES series(id)
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
