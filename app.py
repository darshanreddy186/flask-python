from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize SQLite database for storing expenses
def init_db():
    with sqlite3.connect('expenses.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS expenses
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         category TEXT, 
                         amount REAL)''')

# Home page to display all expenses and total
@app.route('/')
def home():
    with sqlite3.connect('expenses.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
        total_expense = cursor.execute("SELECT SUM(amount) FROM expenses").fetchone()[0]
    return render_template('index.html', expenses=expenses, total=total_expense)

# Add expense
@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form['category']
    amount = float(request.form['amount'])
    with sqlite3.connect('expenses.db') as conn:
        conn.execute('INSERT INTO expenses (category, amount) VALUES (?, ?)', (category, amount))
    return redirect(url_for('home'))

# Update expense
@app.route('/update', methods=['POST'])
def update_expense():
    expense_id = int(request.form['id'])
    category = request.form['category']
    amount = float(request.form['amount'])
    with sqlite3.connect('expenses.db') as conn:
        conn.execute('UPDATE expenses SET category = ?, amount = ? WHERE id = ?', (category, amount, expense_id))
    return redirect(url_for('home'))

# Delete expense
@app.route('/delete', methods=['POST'])
def delete_expense():
    expense_id = int(request.form['id'])
    with sqlite3.connect('expenses.db') as conn:
        conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    return redirect(url_for('home'))

# Search expenses
@app.route('/search', methods=['GET'])
def search_expenses():
    search_query = request.args.get('query', '')
    with sqlite3.connect('expenses.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses WHERE category LIKE ?', (f'%{search_query}%',))
        results = cursor.fetchall()
    return render_template('search.html', results=results)

if __name__ == '__main__':
    init_db()
    app.run(port=90)
