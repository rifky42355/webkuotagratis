from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from pymongo import MongoClient
from flask_mail import Mail, Message
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
app = Flask(__name__)
app.secret_key = 'super_secret_key_12345'


# Konfigurasi MongoDB
collection = db['userdata']

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Ganti sesuai penyedia email
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'muhammadrifkyfadillah123@gmail.com'  # Email Anda
app.config['MAIL_PASSWORD'] = 'lmrc obmb nqey hcwk'         # Kata sandi email Anda
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    phone = request.form.get('phone')

    if not name or not phone:
        return jsonify({"error": "Nama dan nomor HP wajib diisi"}), 400

    # Simpan data ke MongoDB
    data = {"name": name, "phone": phone}
    collection.insert_one(data)

    try:
        msg = Message(
            subject='Notifikasi Data Baru Masuk',
            sender='your_email@gmail.com',  # Email pengirim
            recipients=['recipient_email@gmail.com'],  # Email penerima
            body=f"Data baru telah masuk:\n\nNama: {name}\nNomor HP: {phone}"
        )
        mail.send(msg)
        flash('Data anda telah diterima, mohon tunggu kuota masuk', 'success')
    except Exception as e:
        flash(f'Data berhasil disimpan, tetapi email gagal dikirim: {e}', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
