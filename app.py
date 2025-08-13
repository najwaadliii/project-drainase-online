from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- Konfigurasi Penting ---
# Mengambil kunci rahasia dari environment variable untuk keamanan
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'kunci-default-untuk-testing-lokal')

# Mengambil URL Database dari environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Model Database ---
class Pengukuran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_titik = db.Column(db.String(100), nullable=False)
    sudut_horizontal = db.Column(db.Float, nullable=False)
    sudut_vertikal = db.Column(db.Float, nullable=False)
    jarak = db.Column(db.Float, nullable=False)

# --- Sistem Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ganti 'rahasia123' dengan password yang Anda inginkan
        if request.form['password'] == 'rahasia123':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Password salah!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# --- Halaman Utama ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        data_baru = Pengukuran(
            nama_titik=request.form['nama_titik'],
            sudut_horizontal=float(request.form['sudut_horizontal']),
            sudut_vertikal=float(request.form['sudut_vertikal']),
            jarak=float(request.form['jarak'])
        )
        db.session.add(data_baru)
        db.session.commit()
        return redirect(url_for('index'))
    
    data_pengukuran = Pengukuran.query.order_by(Pengukuran.id.desc()).all()
    return render_template('index.html', data_pengukuran=data_pengukuran)