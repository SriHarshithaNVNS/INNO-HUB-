from flask import Flask, request, render_template, redirect, url_for
import random
import smtplib
from email.message import EmailMessage
import mysql.connector
from mysql.connector import Error
import os


connection = mysql.connector.connect(
    host="localhost", 
    username="root", 
    password="root", 
    database="innovator"
    )
my_cursor = connection.cursor()

app = Flask(__name__)
ootp = ""
id = 0

# Generate a random OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Send OTP to email
def send_otp(email, otp):
    msg = EmailMessage()
    msg.set_content(f"Your OTP is: {otp}")
    msg['Subject'] = 'Reset Password OTP'
    msg['From'] = 'resetinnohub@gmail.com'  # Sender's email
    msg['To'] = email

    # Replace 'smtp.gmail.com' with your SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('resetinnohub@gmail.com', 'odwf xrpg bxbt ynlb')  # Replace with your email credentials
        server.send_message(msg)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'Innovator':
            return render_template('innologin.html')
        elif action == 'Investor':
            return render_template('invlogin.html')
    return render_template('form.html')


@app.route('/innologin', methods=['GET', 'POST'])
def innologin():
    login_failed = False
    if request.method == 'POST':
        email = request.form['mailid']
        password = request.form['pass']

        # Query to fetch user data based on the provided email
        query = "SELECT * FROM login WHERE email = %s"
        my_cursor.execute(query, (email,))
        user = my_cursor.fetchone()

        if user and user[1] == password:  # Assuming user[1] is the password column
            # Redirect if email and password match
            global id
            id = user[2]
            return redirect(url_for('uploaded'))
            
        else:
            login_failed = True
    
    # Redirect to the same page if it's a GET request or if authentication fails
    return render_template('innologin.html', login_failed=login_failed)

@app.route('/invlogin', methods=['GET', 'POST'])
def invlogin():
    login_failed = False
    if request.method == 'POST':
        email = request.form['mailid']
        password = request.form['pass']

        # Query to fetch user data based on the provided email
        query = "SELECT * FROM invlogin WHERE email = %s"
        my_cursor.execute(query, (email,))
        user = my_cursor.fetchone()

        # Debug: Print the fetched user data
        print(f"Fetched user data: {user}")

        if user and user[2] == password:  # Assuming user[1] is the password column
            # Redirect if email and password match
            global id
            id = user[0]  # Adjusted to use the correct user ID column index
            return redirect(url_for('investorhome'))
        else:
            login_failed = True
    
    # Redirect to the same page if it's a GET request or if authentication fails
    return render_template('invlogin.html', login_failed=login_failed)



@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    password_match = True  # Assume passwords match by default
    email_exists = False  # Assume email does not exist by default

    if request.method == 'POST':
        email = request.form['mailid']
        password = request.form['pass']
        confirmpassword = request.form['conpass']
        role = request.form['role']

        if password != confirmpassword:
            password_match = False  # Set to False if passwords don't match
        else:
            # Determine the table based on the role
            if role == 'innovator':
                table = 'login'
                url = 'upload'
            else:  # role == 'investor'
                table = 'invlogin'
                url = 'investorhome'

            # Check if email already exists in the corresponding table
            query = f"SELECT * FROM {table} WHERE email = %s"
            my_cursor.execute(query, (email,))
            existing_user = my_cursor.fetchone()

            if existing_user:
                email_exists = True
            else:
                # Insert new user into the appropriate table
                query = f"INSERT INTO {table} (email, password) VALUES (%s, %s)"
                values = (email, password)
                my_cursor.execute(query, values)
                connection.commit()
                
                # Redirect to the 'upload' endpoint after processing the form data
                return redirect(url_for(url))

    # Pass the password_match and email_exists variables to the template
    return render_template('sign-up.html', password_match=password_match, email_exists=email_exists)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['cat']
        des = request.form['description']
        video = request.files['video']
        if video.filename == '':
            return 'No selected video file'

        # Save the uploaded video file
        video_path = 'videos/' + video.filename
        video.save(video_path)

        # Handle file upload
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # Read the file content
            upload_directory = 'files/'
            file_path = os.path.join(upload_directory, uploaded_file.filename)
            uploaded_file.save(file_path)

            # Store the file path in the database
            sql = "INSERT INTO uploads (pname, cat, des, file_name, video_data) VALUES (%s, %s, %s, %s, %s);"
            values = (name, category, des, file_path, video_path)
            my_cursor.execute(sql, values)
            connection.commit()
            message = 'Uploaded successfully'  # Set your message here
            return render_template('upload.html', message=message)
        else:
            return 'No file selected'
    return render_template('upload.html', message="")    


@app.route('/uploaded', methods=['GET', 'POST'])
def uploaded():
    # Example query to fetch uploaded items

    query = f"SELECT * FROM uploads"
    my_cursor.execute(query)
    items = my_cursor.fetchall()

    # Close the cursor and the connection

    return render_template('uploaded.html', items=items)

@app.route('/investorhome', methods=['GET', 'POST'])
def investorhome():
    query = "SELECT uid, file_name, is_hidden FROM uploads"
    my_cursor.execute(query)
    items = my_cursor.fetchall()

    return render_template('investorhome.html', items=items)



@app.route('/hide_unhide', methods=['POST'])
def hide_unhide():
    doc_id = request.form['doc_id']
    action = request.form['action']
    
    if action == 'Hide':
        query = "UPDATE uploads SET is_hidden = TRUE WHERE uid = %s"
    elif action == 'Unhide':
        query = "UPDATE uploads SET is_hidden = FALSE WHERE uid = %s"
    
    my_cursor.execute(query, (doc_id,))
    connection.commit()
    
    return redirect(url_for('investorhome'))


@app.route('/log_out', methods=['GET', 'POST'])
def log_out():
    return render_template('logout.html')
       

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    global ootp
    if request.method == 'POST':
        email = request.form['email']
        ootp = generate_otp()
        send_otp(email, ootp)
        return render_template('verify_otp.html', email=email)
    return render_template('reset_password.html')

# @app.route('/verify', methods=['POST'])
# def verify_otp():
#     global ootp
#     email = request.form['email']
#     otp = request.form['otp']
#     print(ootp)
#     if ootp == otp:
#         return "OTP verification successful"
#     return "invalid OTP"

@app.route('/verify', methods=['POST'])
def verify_otp():
    global ootp
    otp = request.form['otp']
    if ootp == otp:
        return render_template('confirm_password.html')
    return "Invalid OTP"

@app.route('/confirm_password', methods=['POST'])
def confirm_password():
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if password == confirm_password:
        # Reset the password (perform your password reset logic here)
        return render_template('/form.html')
    return "Passwords do not match"

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
