import cv2
from flask import Flask, render_template, request, redirect, session, send_file,url_for
from flask_mail import Mail, Message
from authlib.integrations.flask_client import OAuth
from flask import session, url_for
from dotenv import load_dotenv
load_dotenv()

import sqlite3
import pandas as pd
import qrcode
import os

app = Flask(__name__)

app.secret_key = "eventportal123"

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv('213890701257-beml8qntavr0e5mted5uc6al2qfsdpku.apps.googleusercontent.com'),
    client_secret=os.getenv('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'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

app.config['MAIL_USERNAME'] = 'harivasan068@gmail.com'
app.config['MAIL_PASSWORD'] = 'qmidzjjqvogsgykm'

mail = Mail(app)

app.secret_key = "event_secret_key"


# ==========================
# HOME PAGE
# ==========================

@app.route('/')
def home(): 
    return render_template('index.html')


# ==========================
# REGISTRATION PAGE
# ==========================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        event = request.form['event']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            event TEXT
        )
        """)

        cursor.execute("""
INSERT INTO registrations(name,email,phone,event)
VALUES(?,?,?,?)
""", (name, email, phone, event))

        conn.commit()
        conn.close()

        # Generate QR Code
        qr_data = f"""
Name: {name}
Email: {email}
Phone: {phone}
Event: {event}
"""

        img = qrcode.make(qr_data)

        filename = f"{name}.png"

        os.makedirs("static/qrcodes", exist_ok=True)

        filepath = os.path.join(
            "static",
            "qrcodes",
            filename
        )

        img.save(filepath)
        
                # Send Email with QR Attachment
        try:

            msg = Message(
                "Event Registration Successful",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email]
            )

            msg.body = f"""
Hello {name},

Thank you for registering for Tech Fest 2026.

Your registration has been confirmed.

Your QR code is attached with this email.

Regards,
Event Registration Team
"""

            with app.open_resource(filepath) as qr_file:
                msg.attach(
                    filename,
                    "image/png",
                    qr_file.read()
                )

            mail.send(msg)

            print("EMAIL SENT SUCCESSFULLY")

        except Exception as e:

            print("EMAIL ERROR:", e)
        return render_template(
            "success.html",
            qr_image=filename
        )

    return render_template('register.html')


# ==========================
# ADMIN LOGIN
# ==========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":

            session['admin'] = True

            return redirect('/admin')

        else:

            return """
            <h2>Invalid Login</h2>
            <a href='/login'>Try Again</a>
            """

    return render_template('login.html')


# ==========================
# ADMIN DASHBOARD
# ==========================

@app.route('/admin')
def admin():

    if 'admin' not in session:
        return redirect('/login')

    search = request.args.get('search', '')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM registrations
    WHERE name LIKE ?
    OR email LIKE ?
    OR phone LIKE ?
    """,
    (
        f'%{search}%',
        f'%{search}%',
        f'%{search}%'
    ))

    data = cursor.fetchall()

    total = len(data)

    cursor.execute(
        "SELECT COUNT(*) FROM attendance WHERE event='Tech Fest'"
    )
    techfest_attendance = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM attendance WHERE event='AI Workshop'"
    )
    aiworkshop_attendance = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM attendance WHERE event='Hackathon'"
    )
    hackathon_attendance = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'admin.html',
        data=data,
        total=total,
        techfest_attendance=techfest_attendance,
        aiworkshop_attendance=aiworkshop_attendance,
        hackathon_attendance=hackathon_attendance,
        search=search
    )


# ==========================
# DELETE REGISTRATION
# ==========================

@app.route('/delete/<int:id>')
def delete(id):

    if 'admin' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM registrations WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/admin')


# ==========================
# EXPORT TO EXCEL
# ==========================

@app.route('/export')
def export():

    if 'admin' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')

    df = pd.read_sql_query(
        "SELECT * FROM registrations",
        conn
    )

    conn.close()

    file_name = "registrations.xlsx"

    df.to_excel(
        file_name,
        index=False
    )

    return send_file(
        file_name,
        as_attachment=True
    )


# ==========================
# LOGOUT
# ==========================

@app.route('/logout')
def logout():

    session.pop('admin', None)

    return redirect('/login')


# ==========================
# RUN APP
# ==========================
@app.route('/create_attendance')
def create_attendance():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        event TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

    return "Attendance Table Created"

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():

    if request.method == 'POST':

        name = request.form['name']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO attendance(name,status)
            VALUES(?,?)
            """,
            (name, "Present")
        )

        conn.commit()
        conn.close()

        return render_template(
            'attendance_success.html',
            name=name
        )

    return render_template('attendance.html')


@app.route('/attendance_records')
def attendance_records():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM attendance")

    data = cursor.fetchall()

    conn.close()

    return render_template(
        'attendance_records.html',
        data=data
    )


# ==========================
# QR SCANNER
# ==========================

@app.route('/scan_qr', methods=['GET', 'POST'])
def scan_qr():

    if request.method == 'POST':

        qr_data = request.form['qr_data']

        lines = qr_data.strip().split('\n')

        name = lines[0].replace("Name:", "").strip()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM attendance WHERE name=?",
            (name,)
        )

        existing = cursor.fetchone()

        if not existing:

            cursor.execute("""
            INSERT INTO attendance(name,status)
            VALUES(?,?)
            """, (name, "Present"))

            conn.commit()

        conn.close()

        return f"{name} Attendance Marked Successfully"

    return render_template('scan_qr.html')


# ==========================
# RUN APP
# ==========================


@app.route('/start_scanner')
def start_scanner():

    cap = cv2.VideoCapture(0)

    detector = cv2.QRCodeDetector()

    while True:

        success, frame = cap.read()

        if not success:
            break

        data, bbox, _ = detector.detectAndDecode(frame)

        if data:

            lines = data.strip().split('\n')

            name = lines[0].replace("Name:", "").strip()
            event = lines[3].replace("Event:", "").strip()

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM attendance WHERE name=?",
                (name,)
            )

            existing = cursor.fetchone()

            if existing:

                conn.close()

                cap.release()
                cv2.destroyAllWindows()

                return f"{name} has already marked attendance"

            else:

                cursor.execute("""
                INSERT INTO attendance(name,event,status)
                VALUES(?,?,?)
                """, (name, event, "Present"))

                conn.commit()

                conn.close()

                cap.release()
                cv2.destroyAllWindows()

                return f"{name} Attendance Marked Successfully"

        cv2.imshow("QR Attendance Scanner", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return "Scanner Closed"
@app.route('/reset_attendance')
def reset_attendance():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS attendance")

    conn.commit()
    conn.close()

    return "Attendance Table Deleted"

@app.route('/mobile_scanner')
def mobile_scanner():

    return render_template('mobile_scanner.html')


@app.route('/mobile_scan', methods=['POST'])
def mobile_scan():

    qr_data = request.form['qr_data']

    lines = qr_data.strip().split('\n')

    name = lines[0].replace("Name:", "").strip()
    event = lines[3].replace("Event:", "").strip()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM attendance WHERE name=?",
        (name,)
    )

    existing = cursor.fetchone()

    if not existing:

        cursor.execute("""
        INSERT INTO attendance(name,event,status)
        VALUES(?,?,?)
        """, (name, event, "Present"))

        conn.commit()

    conn.close()

    return f"{name} Attendance Marked Successfully"


@app.route('/google_login')
def google_login():

    return google.authorize_redirect(
        url_for(
            'callback',
            _external=True
        )
    )


@app.route('/callback')
def callback():

    token = google.authorize_access_token()

    user = token['userinfo']

    session['user_name'] = user['name']
    session['user_email'] = user['email']

    return redirect('/')


@app.route('/google_logout')
def google_logout():

    session.clear()

    return redirect('/')


if __name__ == '__main__':

    app.run(debug=True)
