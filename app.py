from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)


# --- (Your existing MySQL configurations) ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' # Enter your MySQL password here
app.config['MYSQL_DB'] = 'feedback_db'

mysql = MySQL(app)


@app.route('/')
def index():
    """Renders the feedback form and displays feedback."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, email, message, is_accepted FROM feedback ORDER BY submission_date DESC")
    feedback_data = cur.fetchall()
    cur.close()
    return render_template('index.html', feedback=feedback_data)


@app.route('/submit', methods=['POST'])
def submit():
    """Handles form submission and inserts data into the database."""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('index'))


@app.route('/accept-all', methods=['POST'])
def accept_all():
    """Accepts all feedback entries."""
    try:
        cur = mysql.connection.cursor()
        # The WHERE clause is important to avoid updating already accepted items unnecessarily
        cur.execute("UPDATE feedback SET is_accepted = TRUE WHERE is_accepted = FALSE")
        mysql.connection.commit()
        affected_rows = cur.rowcount
        cur.close()
        return jsonify({'message': f'{affected_rows} feedback entries accepted successfully!'})
    except Exception as e:
        # Log the error e
        return jsonify({'error': 'An error occurred.'}), 500


if __name__ == '__main__':
    app.run(debug=True)





