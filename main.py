import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from forms import CourseForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Database initialization
def init_db():
    with sqlite3.connect('C:/Users/Bongeka.Mpofu/DB Browser for SQLite/courses.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                price INTEGER NOT NULL,
                level TEXT NOT NULL,
                available BOOLEAN NOT NULL
            )
        ''')
        conn.commit()

# Route for the index page with form submission
@app.route('/', methods=('GET', 'POST'))
def index():
    form = CourseForm()

    # Debugging: Check form submission
    if request.method == 'POST':
        print("POST request received")

    if form.validate_on_submit():
        print("Form validated")  # Debugging line

        # Capture form data
        title = form.title.data
        description = form.description.data
        price = form.price.data
        level = form.level.data
        available = form.available.data

        # Debugging: Print captured form data
        print(f"Title: {title}, Description: {description}, Price: {price}, Level: {level}, Available: {available}")

        # Save data to the SQLite database
        with sqlite3.connect('C:/Users/Bongeka.Mpofu/DB Browser for SQLite/courses.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO courses (title, description, price, level, available)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, description, price, level, available))
            conn.commit()

        # Debugging: Confirmation of successful insertion
        print("Data inserted successfully")

        # Redirect after submitting
        return redirect(url_for('index'))
    else:
        # Debugging: Print form errors if not validated
        print("Form validation failed:", form.errors)

    return render_template('index.html', form=form)

# Run the app and create the database if it doesn't exist
if __name__ == '__main__':
    init_db()
    app.run(debug=True)