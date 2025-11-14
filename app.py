import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

load_dotenv() # loads variables from .env file

app = Flask(__name__, template_folder='./client/templates', static_folder='./client/static') # Point to the root static folder

# --- (Your existing MySQL configurations) ---
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD') # IMPORTANT: Enter your actual MySQL password here
app.config['MYSQL_DB'] = 'feedback_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# --- Flask-Login Setup ---
app.secret_key = os.getenv('SECRET_KEY', 'a-super-secret-key-for-sessions') # Add a SECRET_KEY to your .env file
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirect to /login if user is not authenticated

class User(UserMixin):
    """User model for Flask-Login."""
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    """Load user from the database."""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT id, username, role FROM users WHERE id = %s", (user_id,))
        user_data = cur.fetchone()
        if user_data:
            return User(id=user_data['id'], username=user_data['username'], role=user_data['role'])
    return None

def admin_required(f):
    """Decorator to restrict access to admin-only pages."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Authentication Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT id, username, password, role FROM users WHERE username = %s", (username,))
            user_data = cur.fetchone()
            if user_data and check_password_hash(user_data['password'], password):
                user = User(id=user_data['id'], username=user_data['username'], role=user_data['role'])
                login_user(user)
                if user.role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('reviewer_dashboard'))
        flash('Invalid username or password.', 'error') # This line is reached if login fails
    return render_template('login.html') # Re-render the login page on GET or failed POST

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        try:
            with mysql.connection.cursor() as cur:
                # All new registrations will have the 'user' role.
                cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, 'user'))
                mysql.connection.commit()
            return redirect(url_for('login'))
        except mysql.connection.IntegrityError:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Logs the user out."""
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    """Redirects user to their respective dashboard."""
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('reviewer_dashboard'))

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    """Renders the admin dashboard with all feedback."""
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT id, name, email, message, movie_title, rating, is_accepted, submission_date FROM feedback ORDER BY submission_date DESC")
        feedback_data = cur.fetchall()
    return render_template('admin_dashboard.html', feedback=feedback_data, current_user=current_user)

@app.route('/dashboard')
@login_required
def reviewer_dashboard():
    """Renders the reviewer dashboard to submit feedback."""
    return render_template('reviewer_dashboard.html', current_user=current_user)

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    """Handles movie feedback submission and inserts data into the database."""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        movie_title = request.form['movie_title'] # Capture the movie title from the form
        rating = request.form['rating'] # Capture the rating from the form

        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO feedback (name, email, message, movie_title, rating) VALUES (%s, %s, %s, %s, %s)", (name, email, message, movie_title, rating))
            mysql.connection.commit()
        flash('Your feedback has been submitted successfully!', 'success')
    return redirect(url_for('reviewer_dashboard'))


@app.route('/accept-all', methods=['POST'])
@login_required
@admin_required
def accept_all():
    """Accepts all feedback entries."""
    try:
        with mysql.connection.cursor() as cur:
            # The WHERE clause is important to avoid updating already accepted items unnecessarily
            cur.execute("UPDATE feedback SET is_accepted = TRUE WHERE is_accepted = FALSE")
            mysql.connection.commit()
            return jsonify({'message': f'{cur.rowcount} feedback entries accepted successfully!'})
    except Exception as e:
        # Log the error e
        return jsonify({'error': 'An error occurred.'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8080)
