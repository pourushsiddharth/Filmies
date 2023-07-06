# import sqlite3

# # Connect to the SQLite database
# conn = sqlite3.connect("movie.db")
# cursor = conn.cursor()

# # Create the series table
# cursor.execute('''
#     CREATE TABLE series (
#         id INTEGER PRIMARY KEY,
#         name TEXT,
#         description TEXT,
#         genre TEXT,
#         drive_id TEXT,
#         trailer_id TEXT,
#         ott_platform TEXT,
#         for_kids INTEGER
#     )
# ''')

# # Commit the changes and close the connection
# conn.commit()
# conn.close()

# import sqlite3

# # Connect to the SQLite database
# conn = sqlite3.connect("movie.db")
# cursor = conn.cursor()

# # Drop the series table
# cursor.execute("DROP TABLE IF EXISTS series")

# # Commit the changes and close the connection
# conn.commit()
# conn.close()

# import sqlite3

# def create_episodes_table():
#     # Connect to the SQLite database
#     conn = sqlite3.connect("movie.db")
#     cursor = conn.cursor()

#     # Create the episodes table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS episodes (
#             id INTEGER PRIMARY KEY,
#             series_id INTEGER,
#             episode_number INTEGER,
#             drive_id TEXT,
#             FOREIGN KEY (series_id) REFERENCES series(id)
#         )
#     ''')

#     # Commit the changes and close the connection
#     conn.commit()
#     conn.close()

import sqlite3

# Connect to the database
connection = sqlite3.connect('movie.db')
cursor = connection.cursor()

# Execute the ALTER TABLE statement to add the "series_name" column
alter_query = "ALTER TABLE series ADD COLUMN primary_color TEXT"
cursor.execute(alter_query)

# Commit the changes and close the connection
connection.commit()
connection.close()

# import sqlite3


# def create_stories_table():
#     # Connect to the SQLite database
#     conn = sqlite3.connect("movie.db")
#     cursor = conn.cursor()

#     # Create the stories table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS stories (
#             id INTEGER PRIMARY KEY,
#             user_id INTEGER,
#             content TEXT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (user_id) REFERENCES users(id)
#         )
#     ''')

#     # Commit the changes and close the connection
#     conn.commit()
#     conn.close()



# #delete table code
# import sqlite3

# # Connect to the SQLite database
# conn = sqlite3.connect("movie.db")
# cursor = conn.cursor()

# # Delete the episodes table
# cursor.execute("DROP TABLE IF EXISTS episodes")

# # Delete the seasons table
# cursor.execute("DROP TABLE IF EXISTS seasons")

# # Delete the series table
# cursor.execute("DROP TABLE IF EXISTS series")

# # Commit the changes and close the connection
# conn.commit()
# conn.close()





# @app.route('/about_series/<int:series_id>')
# def about_series(series_id):
#     # Fetch series details from the database
#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM series WHERE series_id = ?", (series_id,))
#     series = cursor.fetchone()

#     if series is None:
#         return "Series not found"
    
#     name = series[1]
#     description = series[2]
#     genre = series[3]
#     ott_platform = series[5]
#     logo_url = series[6]
#     poster_url = series[8]
#     director = series[9]

#     # Fetch seasons for the series from the database
#     cursor.execute("SELECT * FROM seasons WHERE series_id = ?", (series_id,))
#     seasons = cursor.fetchall()

#     if len(seasons) == 0:
#         return "No seasons found for the series"
    
#     # Fetch episodes for the series from the database
#     cursor.execute("SELECT * FROM episodes WHERE season_id = ?", (seasons[0][0],))
#     episodes = cursor.fetchall()

#     if len(episodes) == 0:
#         return "No episodes found for the series"
    
#     drive_id = episodes[0][2]
#     episode_id = episodes[0][0]

#     return render_template('about_series.html', series=series, seasons=seasons, name=name, description=description, genre=genre, ott_platform=ott_platform, logo_url=logo_url, poster_url=poster_url, director=director, drive_id=drive_id, episode_id=episode_id)

