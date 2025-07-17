# app/routes.py
from flask import render_template, request, redirect, url_for, jsonify
import psycopg2
import json
from app import app
from config import DB_PARAMS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        names = request.form.getlist('name[]')

        try:
            conn = psycopg2.connect(**DB_PARAMS)
            cur = conn.cursor()
            cur.execute("INSERT INTO submissions (data) VALUES (%s)", [json.dumps(names)])
            conn.commit()
        except Exception as e:
            print(f"Ошибка при работе с базой данных: {e}")
            return "Ошибка сервера при сохранении данных", 500
        finally:
            if conn:
                cur.close()
                conn.close()

        return redirect(url_for('view_data'))

    return render_template('form.html')


@app.route('/view')
def view_data():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("SELECT data FROM submissions")
        results = cur.fetchall()
        data = [row[0] for row in results]
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return "Ошибка сервера при получении данных", 500
    finally:
        if conn:
            cur.close()
            conn.close()

    return jsonify(data)
