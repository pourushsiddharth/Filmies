from datetime import datetime
import sqlite3
import sys
from flask import Flask, abort, jsonify, render_template, request, redirect, url_for, g
import urllib.parse
import base64
import secrets
from flask import Flask, flash, redirect, request, render_template, session, url_for
from flask_mail import Mail, Message
from functools import wraps
import os


app = Flask(__name__)
DATABASE = 'movie.db'
app.config['SECRET_KEY'] = '71734b7a34dc37e9692aa1a691869b3d'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'alishapanday69@gmail.com'
app.config['MAIL_PASSWORD'] = 'vwzxlyfotxkekfsc'

mail = Mail(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create episode table
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
    
@app.route('/')
def index():
    with sqlite3.connect('movie.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies ORDER BY id DESC")
        movies = cursor.fetchall()
        cursor.execute("SELECT * FROM series ORDER BY series_id DESC")  # Add the ORDER BY clause
        series = cursor.fetchall()

    return render_template('index.html', movies=movies, series=series)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


def generate_unique_key():
    # Generate a random string of 16 bytes and encode it using base64
    key_bytes = secrets.token_bytes(16)
    unique_key = base64.urlsafe_b64encode(key_bytes).decode('utf-8')
    return unique_key

# Dictionary to store movie view counts
view_counts = {}

@app.route('/increment-view-count/<movie_id>', methods=['POST'])
def increment_view_count(movie_id):
    if movie_id in view_counts:
        view_counts[movie_id] += 1
    else:
        view_counts[movie_id] = 1
    
    return jsonify(success=True)

@app.route('/get-view-count/<movie_id>')
def get_view_count(movie_id):
    count = view_counts.get(movie_id, 0)
    return jsonify(view_count=count)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            return redirect(url_for('add_movie'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        description2 = request.form['description2']
        drive_id = request.form['drive_id']
        release_date = request.form['release_date']
        director = request.form['director']
        genre = request.form['genre']
        watch_url = request.form['watch_url']
        poster_url = request.form['poster_url']
        upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        movie_audio = request.form['movie_audio']
        movie_size = request.form['movie_size']
        logo_url = request.form['logo_url']
        thumbnail_url = request.form['thumbnail_url']
        genre_2 = request.form['genre_2']
        genre_3 = request.form['genre_3']
        genre_4 = request.form['genre_4']
        genre_5 = request.form['genre_5']
        wood = request.form['wood']
        imdb = request.form['imdb']
        primary_color = request.form['primary_color']
        on_primary_color = request.form['on_primary_color']
        ott_platform = request.form['ott_platform']
        for_kids = 'yes' if 'for_kids' in request.form else 'no'
        beta_version = 'yes' if 'beta_version' in request.form else 'no'
        likes = 0
        dislikes = 0
        unique_key = generate_unique_key()

        conn = get_db()
        cursor = conn.cursor()
        # Insert movie data into database
        cursor.execute("INSERT INTO movies (unique_key, title, description, description2, drive_id, release_date, director, genre, watch_url, poster_url, upload_time, movie_audio, movie_size, logo_url, thumbnail_url, likes, dislikes, genre_2, genre_3, genre_4, genre_5, wood, for_kids, beta_version, imdb, ott_platform, primary_color, on_primary_color) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (unique_key, title, description, description2, drive_id, release_date, director, genre, watch_url, poster_url, upload_time, movie_audio, movie_size, logo_url, thumbnail_url, likes, dislikes, genre_2, genre_3, genre_4, genre_5, wood, for_kids, beta_version, imdb, ott_platform, primary_color, on_primary_color))
        conn.commit()

        return redirect(url_for('index'))
    else:
        return render_template('add.html')

@app.route('/series2/<string:series_id>')
def series2(series_id):
   # Connect to the SQLite database
    conn = sqlite3.connect('movie.db')
    c = conn.cursor()

    # Fetch series details
    series_query = c.execute('SELECT * FROM series WHERE series_id = ?', (series_id,))
    series = series_query.fetchone()

    # Fetch seasons for the series
    seasons_query = c.execute('SELECT * FROM seasons WHERE series_id = ?', (series_id,))
    seasons = seasons_query.fetchall()

    # Close the database connection
    conn.close()

    return render_template('about_series2.html', series=series, seasons=seasons)


@app.route('/watch_series2/<int:series_id>/<int:season_number>/<int:episode_number>')
def watch_series2(series_id, season_number, episode_number):
    # Fetch series details from the database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM series WHERE series_id = ?", (series_id,))
    series = cursor.fetchone()

    if series is None:
        return "Series not found"
    
    # Fetch the selected season_id from the database
    cursor.execute("SELECT * FROM seasons WHERE series_id = ? AND season_number = ?", (series_id, season_number))
    season = cursor.fetchone()

    if season is None:
       return "Selected season not found"

    season_id = season[0]
    season_number = season[2]

    # Retrieve recommended movies from the database
    cursor.execute("SELECT * FROM series WHERE genre = ? OR genre_2 = ? OR genre_3 = ? OR genre_4 = ? OR genre_5 = ? AND series_id != ? LIMIT 5", (series[3], series[10], series[11], series[12], series[13], series_id,))
    current_series = cursor.fetchall()

    # Fetch episodes for the season from the database using the retrieved season_id
    cursor.execute("SELECT * FROM episodes WHERE season_id = ?", (season_id,))
    episodes = cursor.fetchall()

    if len(episodes) == 0:
        return "No episodes found for the series"
    
    cursor.execute("SELECT * FROM series WHERE series_id = ?", (series_id,))
    series = cursor.fetchone()

    cursor.execute("SELECT * FROM seasons WHERE series_id = ?", (series_id,))
    seasons = cursor.fetchall()
    
    if len(seasons) == 0:
        return "No seasons found for the series"
    

    # Fetch the selected episode from the database
    cursor.execute("SELECT * FROM episodes WHERE season_id = ? AND episode_number = ?", (season_id, episode_number,))
    episode = cursor.fetchone()

    if episode is None:
        return "Selected episode not found"
    
    drive_id = episode[2]
    episode_id = episode[0]
    episode_number = episode[3]

    previous_episode_id = None
    next_episode_id = None

    for i, e in enumerate(episodes):
        if e[0] == episode_id:
            if i > 0:
                previous_episode_id = episodes[i - 1][0]
            if i < len(episodes) - 1:
                next_episode_id = episodes[i + 1][0]
            break

    return render_template('watch_series2.html', series=series, season=season, episodes=episodes, episode=episode, previous_episode_id=previous_episode_id, current_series=current_series, next_episode_id=next_episode_id, drive_id=drive_id, episode_id=episode_id, episode_number=episode_number, season_id=season_id, season_number=season_number, seasons = seasons,)


@app.route('/like/<unique_key>')
def like_movie(unique_key):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE movies SET likes = likes + 1 WHERE unique_key = ?", (unique_key,))
    conn.commit()
    return redirect(url_for('watch', unique_key=unique_key))

@app.route('/dislike/<unique_key>')
def dislike_movie(unique_key):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE movies SET dislikes = dislikes + 1 WHERE unique_key = ?", (unique_key,))
    conn.commit()
    return redirect(url_for('watch', unique_key=unique_key))

@app.route('/movies')
def movies():
    with sqlite3.connect('movie.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()

    return render_template('movies.html', movies=movies)

@app.route('/genre/<genre_name>')
def movies_by_genre(genre_name):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE genre = ? OR genre_2 = ? OR genre_3 = ? OR genre_4 = ? OR genre_5 = ?", (genre_name, genre_name, genre_name, genre_name, genre_name))
    movies = cursor.fetchall()
    cursor.execute("SELECT * FROM series WHERE genre = ? OR genre_2 = ? OR genre_3 = ? OR genre_4 = ? OR genre_5 = ?", (genre_name, genre_name, genre_name, genre_name, genre_name))
    series = cursor.fetchall()

    return render_template('genre.html', movies=movies, genre=genre_name, series = series)

@app.route('/watch/<string:unique_key>')
def watch(unique_key):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE unique_key = ?", (unique_key,))
    movie = cursor.fetchone()

    if movie is None:
        abort(404)  # Movie not found

    likes = movie[12]
    dislikes = movie[13]

    url = request.url
    encoded_url = urllib.parse.quote(url, safe='')

    # Retrieve recommended movies from the database
    cursor.execute("SELECT * FROM movies WHERE genre = ? AND unique_key != ?", (movie[7], unique_key,))
    current_movies = cursor.fetchall()

    # Retrieve recommended movies from the database
    cursor.execute("SELECT * FROM movies WHERE genre_5 = ? AND unique_key != ?", (movie[26], unique_key,))
    parts = cursor.fetchall()

    # Generate the share URL
    share_url = request.host_url + 'watch/' + unique_key

    # Get thumbnail_url and logo_url from the movie record
    thumbnail_url = movie[15]
    logo_url = movie[16]
    drive_id = movie[4]

    return render_template('watch.html', movie=movie, likes=likes, dislikes=dislikes, encoded_url=encoded_url, share_url=share_url, current_movies=current_movies, thumbnail_url=thumbnail_url, logo_url=logo_url, drive_id=drive_id, parts=parts)

@app.route('/watch2/<string:unique_key>')
def watch2(unique_key):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE unique_key = ?", (unique_key,))
    movie = cursor.fetchone()

    if movie is None:
        abort(404)  # Movie not found

    likes = movie[12]
    dislikes = movie[13]
    beta_version = movie[19]

    url = request.url
    encoded_url = urllib.parse.quote(url, safe='')

    # Retrieve recommended movies from the database
    cursor.execute("SELECT * FROM movies WHERE genre = ? AND unique_key != ? LIMIT 5", (movie[7], unique_key,))
    current_movies2 = cursor.fetchall()

    # Generate the share URL
    share_url = request.host_url + 'watch2/' + unique_key

    # Get thumbnail_url and logo_url from the movie record
    thumbnail_url = movie[15]
    logo_url = movie[16]
    drive_id = movie[4]

    return render_template('watch2.html', movie=movie, likes=likes, dislikes=dislikes, encoded_url=encoded_url, share_url=share_url, current_movies2=current_movies2, thumbnail_url=thumbnail_url, logo_url=logo_url, drive_id=drive_id)

@app.route('/edit_movie', methods=['GET', 'POST'])
def edit_movie():
    return render_template('edit_movie.html')

@app.route('/update_movie', methods=['POST'])
def update_movie():
    drive_id = request.form['drive_id']
    title = request.form['title']
    description = request.form['description']
    description2 = request.form['description2']
    release_date = request.form['release_date']
    director = request.form['director']
    genre = request.form['genre']
    watch_url = request.form['watch_url']
    poster_url = request.form['poster_url']
    movie_audio = request.form['movie_audio']
    movie_size = request.form['movie_size']
    likes = request.form['likes']
    dislikes = request.form['dislikes']

    conn = sqlite3.connect('movie.db')
    c = conn.cursor()
    c.execute('''
        UPDATE movies
        SET title=?, description=?, description2=?, release_date=?, director=?, genre=?, watch_url=?, poster_url=?, movie_audio=?, movie_size=?, likes=?, dislikes=?
        WHERE drive_id=?
    ''', (title, description, description2, release_date, director, genre, watch_url, poster_url, movie_audio, movie_size, likes, dislikes, drive_id))
    conn.commit()
    conn.close()

    return redirect(url_for('edit_movie'))

@app.route('/delete_movie')
def delete_movie():
    drive_id = request.args.get('drive_id')

    conn = sqlite3.connect('movie.db')
    c = conn.cursor()
    c.execute('DELETE FROM movies WHERE drive_id=?', (drive_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


@app.route('/search_movies/', methods=['POST'])
def search_movies():
    query = request.form['query']

    # Connect to the database
    conn = sqlite3.connect('movie.db')
    c = conn.cursor()

    # Execute the search query for movies
    movie_search_query = "SELECT * FROM movies WHERE title LIKE ? OR description LIKE ? OR description2 LIKE ? OR director LIKE ? OR genre LIKE ?"
    movie_params = ['%' + query + '%'] * 5  # Add wildcard characters to search for partial matches
    c.execute(movie_search_query, movie_params)
    movies = c.fetchall()

    # Execute the search query for series
    series_search_query = "SELECT * FROM series WHERE name LIKE ? OR description LIKE ? OR genre LIKE ? OR director LIKE ?"
    series_params = ['%' + query + '%'] * 4  # Add wildcard characters to search for partial matches
    c.execute(series_search_query, series_params)
    series = c.fetchall()

    # Close the connection
    conn.close()

    return render_template('search_results.html', movies=movies, series=series)

@app.route('/share/<unique_key>', methods=['GET'])
def share(unique_key):
        # Retrieve the movie details from the database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE unique_key = ?", (unique_key,))
    movie = cursor.fetchone()

    if movie is None:
        abort(404)  # Movie not found

    # Retrieve recommended movies from the database
    cursor.execute("SELECT * FROM movies WHERE genre = ? AND unique_key != ? LIMIT 5", (movie[7], unique_key,))
    recommended_movies = cursor.fetchall()

    # Generate the share URL
    share_url = request.host_url + 'watch/' + unique_key

    # Pass the share URL, movie details, and recommended movies to the template
    return render_template('share.html', share_url=share_url, movie=movie, recommended_movies=recommended_movies)

@app.route('/share2/<unique_key>', methods=['GET'])
def share2(unique_key):
        # Retrieve the movie details from the database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE unique_key = ?", (unique_key,))
    movie = cursor.fetchone()

    if movie is None:
        abort(404)  # Movie not found

    # Retrieve recommended movies from the database
    cursor.execute("SELECT * FROM movies WHERE genre = ? AND unique_key != ? LIMIT 5", (movie[7], unique_key,))
    recommended_movies = cursor.fetchall()

    # Generate the share URL
    share_url = request.host_url + 'watch2/' + unique_key

    # Pass the share URL, movie details, and recommended movies to the template
    return render_template('share2.html', share_url=share_url, movie=movie, recommended_movies=recommended_movies)

@app.route('/feedback/<string:unique_key>', methods=['GET', 'POST'])
def feedback(unique_key):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE unique_key = ?", (unique_key,))
    movie = cursor.fetchone()

    if movie is None:
        abort(404)  # Movie not found

    likes = movie[12]
    dislikes = movie[13]

    url = request.url
    encoded_url = urllib.parse.quote(url, safe='')

    # Retrieve recommended movies from the database
    cursor.execute("SELECT * FROM movies WHERE genre = ? AND unique_key != ? LIMIT 5", (movie[7], unique_key,))
    current_movies = cursor.fetchall()

    # Generate the share URL
    share_url = request.host_url + 'watch/' + unique_key

    # Get thumbnail_url and logo_url from the movie record
    thumbnail_url = movie[15]
    logo_url = movie[16]
    drive_id = movie[4]

    if request.method == 'POST':
        name = request.form.get('name')
        checkbox1 = request.form.get('checkbox1')
        checkbox2 = request.form.get('checkbox2')
        checkbox3 = request.form.get('checkbox3')
        feedback_text = request.form.get('feedback_text')
        
        # Create the email message
        msg = Message(name, sender='alishapanday69@gmail.com', recipients=['filmiescompany@gmail.com'])
        msg.body = f'''
        {name}
        Checkbox 1: {checkbox1}
        Checkbox 2: {checkbox2}
        Checkbox 3: {checkbox3}
        Feedback Text: {feedback_text}
        '''
        
        # Send the email
        mail.send(msg)
        
        return redirect(url_for('index'))  # Return a response to indicate successful form submission

    return render_template('feedback.html', movie=movie, likes=likes, dislikes=dislikes, encoded_url=encoded_url, share_url=share_url, current_movies=current_movies, thumbnail_url=thumbnail_url, logo_url=logo_url, drive_id=drive_id)

@app.route('/add_series', methods=['GET', 'POST'])
def add_series():
    if request.method == 'POST':
        # Retrieve the form data
        name = request.form['name']
        description = request.form['description']
        poster_url = request.form['poster_url']
        logo_url = request.form['logo_url']
        director = request.form['director']
        genre = request.form['genre']
        genre_2 = request.form['genre_2']
        genre_3 = request.form['genre_3']
        genre_4 = request.form['genre_4']
        genre_5 = request.form['genre_5']
        trailer_id = request.form['trailer_id']
        wood = request.form['wood']
        for_kids = 1 if 'for_kids' in request.form else 0
        ott_platform = request.form['ott_platform']
        beta_version = 'yes' if 'beta_version' in request.form else 'no'

        # Connect to the database
        conn = sqlite3.connect('movie.db')
        c = conn.cursor()

        # Insert the series data into the "series" table
        c.execute('''
            INSERT INTO series (name, description, poster_url, logo_url, director, genre, genre_2, genre_3, genre_4, genre_5, wood, trailer_id, for_kids, ott_platform, beta_version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, poster_url, logo_url, director, genre, genre_2, genre_3, genre_4, genre_5, wood, trailer_id, for_kids, ott_platform, beta_version))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    else:
        return render_template('add_series.html')

@app.route('/add_seasons', methods=['GET', 'POST'])
def add_seasons():
    if request.method == 'POST':
        # Retrieve the form data
        series_id = request.form.get('series_id')
        season_number = request.form.get('season_number')
        total_episode = request.form.get('total_episode')

        # Check if series_id, season_number, and total_episode are provided
        if series_id is None or season_number is None or total_episode is None:
            return "Missing required data"

        # Convert season_number and total_episode to integers
        try:
            season_number = int(season_number)
            total_episode = int(total_episode)
        except ValueError:
            return "Invalid season number or total episodes"

        # Insert season data into the seasons table
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO seasons (series_id, season_number, total_episode) VALUES (?, ?, ?)",
                       (series_id, season_number, total_episode))
        conn.commit()

        # Fetch the last inserted season_id
        season_id = cursor.lastrowid

        # Insert episodes into the episodes table
        episodes = []
        for i in range(1, total_episode + 1):
            drive_id = request.form.get('episode_' + str(i))
            episode_number = i
            episodes.append((season_id, drive_id, episode_number))

        # Insert episodes using executemany to avoid duplicate episode_id
        cursor.executemany(
            "INSERT INTO episodes (season_id, drive_id, episode_number) VALUES (?, ?, ?)", episodes
        )
        conn.commit()

        return redirect(url_for('index'))
    else:
        # Fetch series data from the database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT series_id, name FROM series")
        series_data = cursor.fetchall()

        return render_template('add_seasons.html', series_data=series_data)

@app.route('/series/<int:series_id>')
def about_series(series_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('movie.db')
    c = conn.cursor()

    # Fetch series details
    series_query = c.execute('SELECT * FROM series WHERE series_id = ?', (series_id,))
    series = series_query.fetchone()

    # Fetch seasons for the series
    seasons_query = c.execute('SELECT * FROM seasons WHERE series_id = ?', (series_id,))
    seasons = seasons_query.fetchall()

    # Close the database connection
    conn.close()

    return render_template('about_series.html', series=series, seasons=seasons)


@app.route('/watch_series/<int:series_id>/<int:season_number>/<int:episode_number>')
def watch_series(series_id, season_number, episode_number):
    # Fetch series details from the database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM series WHERE series_id = ?", (series_id,))
    series = cursor.fetchone()

    if series is None:
        return "Series not found"
    
    
    # Fetch the selected season_id from the database
    cursor.execute("SELECT * FROM seasons WHERE series_id = ? AND season_number = ?", (series_id, season_number))
    season = cursor.fetchone()

    if season is None:
       return "Selected season not found"

    season_id = season[0]
    season_number = season[2]

    # Retrieve recommended movies from the database
    cursor.execute("SELECT * FROM series WHERE genre = ? AND series_id != ? LIMIT 5", (series[3], series_id,))
    current_series = cursor.fetchall()

    # Fetch episodes for the season from the database using the retrieved season_id
    cursor.execute("SELECT * FROM episodes WHERE season_id = ?", (season_id,))
    episodes = cursor.fetchall()

    if len(episodes) == 0:
       return "No episodes found for the series"
    
    # Fetch the selected episode from the database
    cursor.execute("SELECT * FROM episodes WHERE season_id = ? AND episode_number = ?", (season_id, episode_number,))
    episode = cursor.fetchone()

    if episode is None:
        return "Selected episode not found"
    
    drive_id = episode[2]
    episode_id = episode[0]
    episode_number = episode[3]

    previous_episode_id = None
    next_episode_id = None

    for i, e in enumerate(episodes):
        if e[0] == episode_id:
            if i > 0:
                previous_episode_id = episodes[i - 1][0]
            if i < len(episodes) - 1:
                next_episode_id = episodes[i + 1][0]
            break

    return render_template('watch_series.html', series=series, season=season, episodes=episodes, episode=episode, previous_episode_id=previous_episode_id, current_series = current_series, next_episode_id=next_episode_id, drive_id=drive_id, episode_id=episode_id, episode_number=episode_number, season_id = season_id, season_number = season_number)


@app.route('/dmca')
def dmca():
    return render_template('dmca.html')

if __name__ == '__main__':
    app.run(debug=True, port=5006)
