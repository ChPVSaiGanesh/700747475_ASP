from flask import Flask, render_template, request, session, redirect, url_for, flash, make_response
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['PERMANENT_SESSION_LIFETIME'] = 300
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 


def create_upload_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])


create_upload_folder()


db_file = 'accounts.db'

if not os.path.exists(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            profile_picture TEXT,
            role TEXT CHECK(role IN ('user', 'agent')) NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            price TEXT,
            area TEXT,
            bedrooms INTEGER,
            bathrooms INTEGER,
            parking TEXT,
            year_built INTEGER,
            nearby_places TEXT,
            contact TEXT,
            images TEXT,
            rent_or_buy TEXT,
            FOREIGN KEY (user_id) REFERENCES accounts (id)
        )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER,
        user_id INTEGER,
        rating INTEGER CHECK(rating BETWEEN 1 AND 5),
        comment TEXT,
        FOREIGN KEY (property_id) REFERENCES properties (id),
        FOREIGN KEY (user_id) REFERENCES accounts (id)
    )
    ''')
    conn.commit()
    conn.close()


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

def get_db_connection():
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        profile_picture = request.files['profile_picture']

        profile_picture_filename = None
        if profile_picture and allowed_file(profile_picture.filename):
            profile_picture_filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_picture_filename))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO accounts (first_name, last_name, email, phone, username, password, profile_picture, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'user')
        ''', (first_name, last_name, email, phone, username, password, profile_picture_filename))
        conn.commit()
        conn.close()

        flash('User registration successful. Please login.', 'success')
        return redirect(url_for('login_user'))

    return render_template('register_user.html')

@app.route('/add_property', methods=['GET', 'POST'])
def add_property():
    if 'logged_in' in session:
        if request.method == 'POST':
            if 'user_id' not in session:
                flash('User ID is missing from the session.', 'danger')
                return redirect(url_for('login_user'))
            
            user_id = session['user_id']
            print("User ID from session:", user_id)
            
            price = request.form['price']
            area = request.form['area']
            bedrooms = request.form['bedrooms']
            bathrooms = request.form['bathrooms']
            parking = request.form['parking']
            year_built = request.form['year_built']
            nearby_places = request.form['nearby_places']
            contact = request.form['contact']
            rent_or_buy = request.form['rent_or_buy']
            images = request.files.getlist('images')

            image_filenames = []
            for image in images:
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_filenames.append(filename)

            image_filenames_str = ','.join(image_filenames)

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(''' 
                INSERT INTO properties (user_id, price, area, bedrooms, bathrooms, parking, year_built, nearby_places, contact, images, rent_or_buy)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, price, area, bedrooms, bathrooms, parking, year_built, nearby_places, contact, image_filenames_str, rent_or_buy))
            conn.commit()
            conn.close()

            flash('Property added successfully.', 'success')
            return redirect(url_for('property_listings'))

        return render_template('add_property.html')
    else:
        return redirect(url_for('login_user'))

@app.route('/update_property/<int:property_id>', methods=['GET', 'POST'])
def update_property(property_id):
    if 'logged_in' not in session:
        return redirect(url_for('login_user'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM properties WHERE id = ?', (property_id,))
    property_data = cursor.fetchone()
    
    if not property_data:
        flash('Property not found.', 'danger')
        return redirect(url_for('my_properties'))

    if request.method == 'POST':
        price = request.form['price']
        area = request.form['area']
        bedrooms = request.form['bedrooms']
        bathrooms = request.form['bathrooms']
        parking = request.form['parking']
        year_built = request.form['year_built']
        nearby_places = request.form['nearby_places']
        contact = request.form['contact']
        rent_or_buy = request.form['rent_or_buy']
        images = request.files.getlist('images')

        image_filenames = []
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filenames.append(filename)

        image_filenames_str = ','.join(image_filenames)

        cursor.execute('''
            UPDATE properties
            SET price = ?, area = ?, bedrooms = ?, bathrooms = ?, parking = ?, year_built = ?, nearby_places = ?, contact = ?, images = ?, rent_or_buy = ?
            WHERE id = ?
        ''', (price, area, bedrooms, bathrooms, parking, year_built, nearby_places, contact, image_filenames_str, rent_or_buy, property_id))
        conn.commit()
        conn.close()

        flash('Property updated successfully.', 'success')
        return redirect(url_for('my_properties'))

    property_dict = dict(property_data)
    property_dict['images'] = property_dict['images'].split(',') if property_dict['images'] else []
    
    return render_template('update_property.html', property=property_dict)

from flask import Flask, render_template, request, session, redirect, url_for, flash, make_response

@app.route('/delete_property/<int:property_id>', methods=['POST'])
def delete_property(property_id):
    if 'logged_in' not in session:
        return redirect(url_for('login_user'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT images FROM properties WHERE id = ?', (property_id,))
    property_data = cursor.fetchone()
    if property_data:
        images = property_data['images'].split(',') if property_data['images'] else []
        for image in images:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image)
            if os.path.exists(image_path):
                os.remove(image_path)

    cursor.execute('DELETE FROM properties WHERE id = ?', (property_id,))
    conn.commit()
    conn.close()

    flash('Property deleted successfully.', 'success')
    return redirect(url_for('my_properties'))



@app.route('/register_agent', methods=['GET', 'POST'])
def register_agent():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']
        profile_picture = request.files['profile_picture']

        profile_picture_filename = None
        if profile_picture and allowed_file(profile_picture.filename):
            profile_picture_filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_picture_filename))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO accounts (first_name, last_name, email, phone, username, password, profile_picture, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'agent')
        ''', (first_name, last_name, email, phone, username, password, profile_picture_filename))
        conn.commit()
        conn.close()

        flash('Agent registration successful. Please login.', 'success')
        return redirect(url_for('login_agent'))

    return render_template('register_agent.html')

@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = ? AND role = ?', (username, 'user'))
        user = cursor.fetchone()
        conn.close()

        if user:
            if user['password'] == password:
                session.permanent = True
                session['logged_in'] = True
                session['username'] = user['username']
                session['user_id'] = user['id']
                session['role'] = 'user'
                return redirect(url_for('property_listings'))
            else:
                flash('Incorrect password. Please try again.', 'danger')
        else:
            flash('Username does not exist. Please check your username or register.', 'danger')

    return render_template('login_user.html')

@app.route('/login_agent', methods=['GET', 'POST'])
def login_agent():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = ? AND role = ?', (username, 'agent'))
        agent = cursor.fetchone()
        conn.close()

        if agent:
            if agent['password'] == password:
                session.permanent = True
                session['logged_in'] = True
                session['username'] = agent['username']
                session['user_id'] = agent['id']
                session['role'] = 'agent'
                return redirect(url_for('property_listings'))
            else:
                flash('Incorrect password. Please try again.', 'danger')
        else:
            flash('Username does not exist. Please check your username or register.', 'danger')

    return render_template('login_agent.html')




@app.route('/my_properties')
def my_properties():
    if 'logged_in' in session:
        user_id = session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM properties WHERE user_id = ?', (user_id,))
        properties = cursor.fetchall()
        conn.close()
        print("User ID from session:", user_id) 
        properties_list = []
        for row in properties:
            property_dict = dict(row)  
            property_dict['images'] = property_dict['images'].split(',') if property_dict['images'] else []
            properties_list.append(property_dict)

        return render_template('my_properties.html', properties=properties_list)
    else:
        return redirect(url_for('login_user'))

@app.route('/add_review/<int:property_id>', methods=['POST'])
def add_review(property_id):
    if 'logged_in' in session:
        user_id = session['user_id']
        rating = int(request.form['rating'])
        comment = request.form['comment']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reviews (property_id, user_id, rating, comment)
            VALUES (?, ?, ?, ?)
        ''', (property_id, user_id, rating, comment))
        conn.commit()
        conn.close()

        flash('Review submitted successfully!', 'success')
        return redirect(url_for('details', property_id=property_id))
    else:
        return redirect(url_for('login_user'))


@app.route('/')
def home():
    return redirect(url_for('landing'))

@app.route('/property_listings')
def property_listings():
    if 'logged_in' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM properties')
        properties = cursor.fetchall()
        conn.close()

        properties_list = []
        for row in properties:
            property_dict = dict(row)  
            property_dict['images'] = property_dict['images'].split(',') if property_dict['images'] else []
            properties_list.append(property_dict)

        return render_template('listing.html', properties=properties_list)
    else:
        return redirect(url_for('login_user'))



@app.route('/profile')
def profile():
    if 'logged_in' in session:
        username = session['username']
        role = session.get('role')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = ?', (username,))
        profile = cursor.fetchone()
        conn.close()

        if profile:
            return render_template('profile.html', user=profile, is_agent=(role == 'agent'))
        else:
            flash('Profile not found.', 'danger')
            return redirect(url_for('property_listings'))
    else:
        return redirect(url_for('login_user'))


@app.route('/landing', methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        role = request.form['role']
        if role == 'user':
            return redirect(url_for('login_user'))
        elif role == 'agent':
            return redirect(url_for('login_agent'))
    
    return render_template('landing.html')


@app.route('/details/<int:property_id>')
def details(property_id):
    if 'logged_in' in session:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM properties WHERE id = ?', (property_id,))
        property_details = cursor.fetchone()

        cursor.execute('''
            SELECT reviews.*, accounts.username
            FROM reviews
            JOIN accounts ON reviews.user_id = accounts.id
            WHERE property_id = ?
        ''', (property_id,))
        reviews = cursor.fetchall()

        conn.close()

        if property_details:
            property_dict = dict(property_details)
            property_dict['images'] = property_dict['images'].split(',') if property_dict['images'] else []

            reviews_list = [dict(review) for review in reviews]

            return render_template('details.html', property=property_dict, reviews=reviews_list)
        else:
            flash('Property not found.', 'danger')
            return redirect(url_for('property_listings'))
    else:
        return redirect(url_for('login_user'))



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('landing'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
