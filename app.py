from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# --------------------
# BASE DE DATOS
# --------------------
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --------------------
# RUTAS
# --------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db()

    if request.method == 'POST':
        titulo = request.form['titulo']
        conn.execute('INSERT INTO tareas (titulo) VALUES (?)', (titulo,))
        conn.commit()
        return redirect(url_for('index'))

    tareas = conn.execute('SELECT * FROM tareas').fetchall()
    conn.close()
    return render_template('index.html', tareas=tareas)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = get_db()
    conn.execute('DELETE FROM tareas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --------------------
# EJECUTAR
# --------------------
if __name__ == '__main__':
    app.run(debug=True)
