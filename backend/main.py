from flask import Flask, request, render_template, redirect, url_for, jsonify, flash
import mysql.connector
import base64
from flask_cors import CORS
from PIL import Image
import io
import os
app = Flask(__name__,template_folder='../frontend',static_folder='../frontend/static')

app.secret_key = 'petp@wr@dise'


CORS(app)


# MySQL database configuration
mysql_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'PETS'
}

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
     # Connect to the database
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    email = request.form['email']
    # Insert the new user into the database
    query = "SELECT * FROM subscribers WHERE email = %s "
    result=cursor.execute(query, (email, ))
    
    result = cursor.fetchone()

    if result: 
        flash('Already subscribed! We will get in touch soon!', 'success')  
        return redirect(url_for('main'))
    
    query = "INSERT INTO subscribers (email) VALUES (%s);"
    cursor.execute(query, (email,))
    
    conn.commit()
    cursor.close()
    conn.close()
    # Signup successful, display a success message
    flash('Thank you for subscribing!', 'success')  
    return redirect(url_for('main'))

@app.route('/keepintouch', methods=['POST'])
def message1():
    # Connect to the database
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    name = request.form['name']
    password = request.form['password']
    message = request.form['message']
    # Insert the new message into the database
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    result = cursor.execute(query, (name, password,))
    result = cursor.fetchone()
    if result:
        query = "INSERT INTO messages (username, message) VALUES (%s, %s);"
        cursor.execute(query, (name, message,))
        conn.commit() # Add this line to commit the changes to the database
        cursor.close()
        conn.close()
        # Message sent successfully, display a success message
        flash('We have received your message!', 'success')
        return redirect(url_for('main'))
    cursor.close()
    conn.close()
    # Display an error message if the user is not signed up
    flash('Please sign up first or check password!', 'error')
    return redirect(url_for('main'))

@app.route('/register')
def register1():
    return render_template('register.html')

@app.route('/signin')
def signin():
    return render_template('signup.html')

@app.route('/adopt')
def adopt():
    # Connect to the database
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    # Execute a SQL query to count the entries in pets
    cursor.execute("SELECT COUNT(*) FROM pets")
    count = cursor.fetchone()[0]

    # Close the database connection
    cursor.close()
    conn.close()
    return render_template('search.html',count=count)

@app.route('/adopt', methods=['POST','GET'])
def adoption_form():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    # Get form data
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']
    id = request.form['id']
    experience = request.form['experience']
    message = request.form['message']

    query = "SELECT * FROM pets WHERE id = %s "
    result=cursor.execute(query, (id, ))
    
    result = cursor.fetchone()
# multiple entries allowed 
    if result:
    # Insert data into the database
        query = "INSERT INTO adoption_requests (name, email, phone, address, city, state, zip, experience, message, petid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, email, phone, address, city, state, zip, experience, message, id)
        cursor.execute(query, val)
        conn.commit()
        
        # Close the database connection
        cursor.close()
        conn.close()
        
        flash('Adoption Request Sent! We will get back to your shortly.', 'success')
        
        return redirect(url_for('adopt'))
        # return 'success'
            # Close the database connection
    cursor.close()
    conn.close()
    flash('ID doesnot exist! Try Again. ', 'error')
        
    return redirect(url_for('adopt'))

@app.route('/register', methods=['POST'])
def register():
    # retrieve form data
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        pet = request.form.get('pet')
        petname = request.form.get('petname')
        age_years = request.form.get('age-years')
        age_months = request.form.get('age-months')
        breed = request.form.get('breed')
        vaccination = request.form.get('vaccination')
        state = request.form.get('state')
        address = request.form.get('address')
        description = request.form.get('description')
        # Load the image from the form data
        image_file = request.files['image']
        image = Image.open(image_file)

        # Compress the image
        compressed_image = io.BytesIO()
        image.save(compressed_image, format='JPEG', quality=50)
        compressed_image.seek(0)

        
        # print form data
        print(f"Pet: {pet}")
        print(f"Pet name: {petname}")
        print(f"Age (years): {age_years}")
        print(f"Age (months): {age_months}")
        print(f"Breed: {breed}")
        print(f"Vaccination: {vaccination}")
        print(f"State: {state}")
        print(f"Description: {description}")
        # Connect to MySQL database
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        result=cursor.execute(query, (username, password))
        
        result = cursor.fetchone()

        if result:
            # Insert form data into MySQL database
            query = "INSERT INTO pets (username, pet, petname, age_years, age_months, breed, vaccination, state, address, description, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (username, pet, petname, age_years, age_months, breed, vaccination, state, address, description, compressed_image.getvalue())
            cursor.execute(query, values)     
            conn.commit()
            cursor.close()
            conn.close()
            flash('Data and image saved successfully!', 'success')
            return redirect(url_for('register'))
        
        query = "SELECT * FROM users WHERE username = %s"
        result=cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result:
            flash('Incorrect password!', 'error')
            return redirect(url_for('register'))
        
        conn.commit()
        cursor.close()
        conn.close()
        flash('Username not found, please Signup!', 'error')
        return redirect(url_for('register'))
    
    except Exception as e:
        print(e)
        flash('An error occurred. Please try again later.', 'error')
        return redirect(url_for('register'))

@app.route('/fetch', methods=['GET', 'POST'])
def fetch():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    # Define the default SQL query to fetch all rows
    sql_query = "SELECT * FROM pets"


    # Execute the SQL query to get the data
    cursor.execute(sql_query)
    rows = cursor.fetchall()

    # Generate the HTML string for each pet
    pets_html = []
    for row in rows:
        # Convert the image data to base64 string
        img_base64 = base64.b64encode(row[9]).decode('utf-8')
        
        # Generate the HTML string for the current pet
        pet_html = f'<div class="content">\n' \
                   f'<img src="data:image/png;base64,{img_base64}" />\n' \
                   f'<h2 id="pet-name">{row[3]}</h2>\n' \
                   f'<p>Approx age: {row[4]} yrs {row[5]} mnths</p>\n' \
                   f'<p>Breed: {row[6]}</p>\n' \
                   f'<p>Location: {row[8]}</p>\n' \
                   f'<h6>{row[7]}</h6>\n' \
                   f'<button class="adopt-1" petID="{row[1]}" onclick="showDetails({row[1]})">Adopt Now</button>\n' \
                   f'</div>\n'
        pets_html.append(pet_html)

    # Join the HTML strings for all pets into a single string
    pets_html_str = '\n'.join(pets_html)

    # Close the database connection
    conn.close()

    # Return the HTML string
    return pets_html_str



@app.route('/pets/<int:pet_id>')
def get_pet_details(pet_id):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    # Get the pet details from the table
    cursor.execute(f"SELECT * FROM pets WHERE id = {pet_id}")
    row = cursor.fetchone()

    # Close the database connection
    conn.close()

    # Convert the row to a dictionary
    pet = {
        'id': row[1],
        'petname': row[3],
        'pet': row[2],
        'age_years': row[4],
        'age_months': row[5],
        'breed': row[6],
        'vaccination': row[7],
        'state': row[8],
        'image': base64.b64encode(row[9]).decode('utf-8'),
        'description': row[11],
        'address': row[10]
    }
    # Return the pet details as a JSON object
    return jsonify(pet)

@app.route('/signin', methods=['POST'])
def signin1():
    username = request.form.get('text')
    password = request.form.get('password')
    email = request.form.get('email')
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    # Check if the username already exists
    query = "SELECT id FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result:
        # Username already exists, return an error message
        conn.close()
        flash('Username already exists', 'error')
        return redirect(url_for('signin'))

    # Insert the new user into the database
    query = "INSERT INTO users (username, password,email) VALUES (%s, %s, %s);"
    cursor.execute(query, (username, password, email))
    
    conn.commit()
    cursor.close()
    conn.close()
    # Signup successful, display a success message
    flash('Sign-Up Successful!', 'success')
    
    return redirect(url_for('signin'))



if __name__ == '__main__':
	app.run()

