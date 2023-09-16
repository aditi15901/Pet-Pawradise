import unittest
from main import app, mysql
import io
from PIL import Image
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import coverage
from flask import url_for
# import requests

# MySQL database configuration
mysql_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'PETS'
}

class TestPetPawradisePage(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        

        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000/main")  # replace with your webpage URL

        self.username = 'testuser12'
        self.password = 'password12311'
        self.email = 'password123@wer11'
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        values = (self.username, self.password, self.email)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

        
    def tearDown(self):
        # Delete the test subscriber from the database after each test
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        query = "DELETE FROM subscribers WHERE email = %s;"
        cursor.execute(query, ('test@example.com1',))
        conn.commit()
        query = "DELETE FROM users WHERE username = %s"
        values = (self.username,)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        self.driver.quit()
       
    
    def test_main_route(self):
        response = self.app.get('/main')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertIn(b'<title>Pet Pawradise</title>', response.data)

    def test_page_title(self):
        expected_title = "Pet Pawradise"
        self.assertEqual(expected_title, self.driver.title)

    def test_banner_links(self):
        response = self.app.get('/main')
        self.assertEqual(response.status_code, 200)

        banner = BeautifulSoup(response.data, 'html.parser').find('section', {'id': 'home'})
        banner_items = banner.find_all('li', {'class': 'banner-item'})

        for item in banner_items:
            link = item.find('a')
            button_text = item.find('button').get_text().strip()
            if button_text == 'ADOPT':
                self.assertEqual(link['href'], '/adopt')
            elif button_text == 'REGISTER PET':
                self.assertEqual(link['href'], '/register')

    def test_nav_links(self):
        links = [
            {"text": "HOME", "href": "http://127.0.0.1:5000/main#home"},
            {"text": "ABOUT", "href": "http://127.0.0.1:5000/main#about"},
            {"text": "REGISTER PET", "href": "http://127.0.0.1:5000/register"},
            {"text": "ADOPT", "href": "http://127.0.0.1:5000/adopt"},
            {"text": "SUBSCRIBE", "href": "http://127.0.0.1:5000/main#subscribe"},
            {"text": "CONTACT US", "href": "http://127.0.0.1:5000/main#contact"},
            {"text": "SIGN IN", "href": "http://127.0.0.1:5000/signin"},
        ]

        nav_bar = self.driver.find_element(By.CSS_SELECTOR, ".navbar-nav")
        nav_links = nav_bar.find_elements(By.CSS_SELECTOR, "li a")

        for i, link in enumerate(links):
            self.assertEqual(link["text"], nav_links[i].text)
            self.assertEqual(link["href"], nav_links[i].get_attribute("href"))

    def test_subscribe_success(self):
        with self.app as client:
            response = client.post('/subscribe', data=dict(email='test@example.com1'), follow_redirects=True)
            self.assertIn(b'Thank', response.data)
    
    def test_subscribe_already_subscribed(self):
        # Add a subscriber to the database first
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO subscribers (email) VALUES ('test@example.com1')")
        conn.commit()
        cursor.close()
        conn.close()
        
        with self.app as client:
            response = client.post('/subscribe', data=dict(email='test@example.com1'), follow_redirects=True)
            # self.assertEqual(response.status_code, 302)  # Redirect
            self.assertIn(b'Already', response.data)

    def test_valid_message(self):
        # simulate a valid form submission with correct username, password and message
        response = self.app.post('/keepintouch', data=dict(
            name='testuser12',
            password='password12311',
            message='This is a test message'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # check if the success message is flashed
        self.assertIn(b'We have received your message!', response.data)

    def test_invalid_message(self):
        # simulate a form submission with incorrect username or password
        response = self.app.post('/keepintouch', data=dict(
            name='Invalid User',
            password='invalid_password',
            message='This is a test message'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # check if the error message is flashed
        self.assertIn(b'Please sign up first or check password!', response.data)

class TestSignInPage(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        self.app_context = app.app_context()
        self.app_context.push()
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000/signin")  # replace with your webpage URL

    def tearDown(self):
        self.app_context.pop()
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        query = "DELETE FROM users WHERE username = %s"
        values = ("testuser1",)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        self.driver.quit()
       

    def test_page_title(self):
        expected_title = "Sign in"
        self.assertEqual(expected_title, self.driver.title)
    
    def test_nav_links1(self):
        links = [
            {"text": "HOME", "href": "http://127.0.0.1:5000/main"},
            {"text": "REGISTER PET", "href": "http://127.0.0.1:5000/register"},
            {"text": "ADOPT", "href": "http://127.0.0.1:5000/adopt"},
            {"text": "CONTACT US", "href": "http://127.0.0.1:5000/signin#contact"},
        ]

        nav_bar = self.driver.find_element(By.CSS_SELECTOR, ".navbar-nav")
        nav_links = nav_bar.find_elements(By.CSS_SELECTOR, "li a")

        for i, link in enumerate(links):
            self.assertEqual(link["text"], nav_links[i].text)
            self.assertEqual(link["href"], nav_links[i].get_attribute("href"))

    # Test if the sign in page is loaded successfully
    def test_load_signin_page(self):
        with app.test_client() as client:
            response = client.get('/signin')
            self.assertEqual(response.status_code, 200)

    # Test if the sign in form is submitted successfully
    def test_submit_signin_form(self):
        with app.test_client() as client:
            response = client.post('/signin', data=dict(
                text='testuser1',
                password='testpassword1',
                email='testuser@example.com1'
            ), follow_redirects=True)
            self.assertIn(b'Sign', response.data)

    # Test if the error message is displayed if the username already exists
    def test_error_message_for_existing_username(self):
        with app.test_client() as client:
            response = client.post('/signin', data=dict(
                text='testuser1',
                password='testpassword1',
                email='existinguser@example.com1'
            ), follow_redirects=True)
            self.assertIn(b'Username already exists', response.data)


class RegisterTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000/register")  # replace with your webpage URL
        # create a test user for registration
        self.username = 'testuser12'
        self.password = 'password12311'
        self.email = 'password123@wer11'
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        values = (self.username, self.password, self.email)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

    def tearDown(self):
        # remove the test user from the database after testing
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        query = "DELETE FROM users WHERE username = %s"
        values = (self.username,)
        cursor.execute(query, values)
        conn.commit()
        query = "DELETE FROM pets WHERE username = %s"
        values = (self.username,)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        self.driver.quit()
       

    def test_page_title(self):
        expected_title = "Register"
        self.assertEqual(expected_title, self.driver.title)

    def test_nav_links1(self):
        links = [
            {"text": "GO BACK TO HOME", "href": "http://127.0.0.1:5000/main"},
            {"text": "CONTACT US", "href": "http://127.0.0.1:5000/register#contact"},
            {"text": "SIGN IN", "href": "http://127.0.0.1:5000/signin"},
            {"text": "ADOPT", "href": "http://127.0.0.1:5000/adopt"},
        ]

        nav_bar = self.driver.find_element(By.CSS_SELECTOR, ".navbar-nav")
        nav_links = nav_bar.find_elements(By.CSS_SELECTOR, "li a")

        for i, link in enumerate(links):
            self.assertEqual(link["text"], nav_links[i].text)
            self.assertEqual(link["href"], nav_links[i].get_attribute("href"))

    def test_register_successful(self):
        # create a mock image file
        with open('/Users/aditi/Downloads/Pet-Pawradise-main 2/backend/d.jpeg', 'rb') as f:
            image_data = f.read()
        image = io.BytesIO(image_data)
        image.filename = 'test.jpg'

        # define the request data
        data = {
            'username': self.username,
            'password': self.password,
            'pet': 'dog',
            'petname': 'Buddy',
            'age-years': '2',
            'age-months': '6',
            'breed': 'Golden Retriever',
            'vaccination': 'Yes',
            'state': 'California',
            'address': '1234 Main St',
            'description': 'A friendly dog',
            'image': (image, 'test.jpg')
        }

        # make the request
        response = self.app.post('/register', data=data, follow_redirects=True)

        # assert that the response is successful and contains the success message
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Data and image saved successfully!', response.data)


    def test_register_missing_fields(self):
        # define the request data with missing fields
        data = {
            'username': self.username,
            'password': self.password,
            'pet': 'dog',
            'petname': 'Buddy',
            'age-months': '6',
            'breed': 'Golden Retriever',
            'vaccination': 'Yes',
            'state': 'California',
            'address': '1234 Main St',
            'description': 'A friendly dog'
        }

        # make the request
        response = self.app.post('/register', data=data, follow_redirects=True)
        #         # check if there was an error message
        # self.assertNotIn(b'Something went wrong', response.data)

        # assert that the response contains the error message for missing fields
        self.assertIn(b'Please', response.data)

    def test_register_incorrect_password(self):
            # create a mock image file
            with open('/Users/aditi/Downloads/Pet-Pawradise-main 2/backend/d.jpeg', 'rb') as f:
                image_data = f.read()
            image = io.BytesIO(image_data)
            image.filename = 'test.jpg'

            # define the request data with incorrect password
            data = {
                'username': self.username,
                'password': 'wrongpassveavword',
                'pet': 'dog',
                'petname': 'Buddy',
                'age-years': '2',
                'age-months': '6',
                'breed': 'Golden Retriever',
                'vaccination': 'Yes',
                'state': 'California',
                'address': '1234 Main St',
                'description': 'A friendly dog',
                'image': (image, 'test.jpg')
            }

            # make the request
            response = self.app.post('/register', data=data, follow_redirects=True)

            # assert that the response contains the error message for incorrect password
            self.assertIn(b'Incorrect password!', response.data)

    def test_username_not_found(self):
        # define the request data with an unknown username
        data = {
            'username': 'unknown_username',
            'password': 'password123',
            'pet': 'dog',
            'petname': 'Buddy',
            'age-years': '2',
            'age-months': '6',
            'breed': 'Golden Retriever',
            'vaccination': 'Yes',
            'state': 'California',
            'address': '1234 Main St',
            'description': 'A friendly dog'
        }

        # make the request
        response = self.app.post('/register', data=data, follow_redirects=True)

        self.assertIn(b'Username', response.data)

class TestAdoptPage(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000/adopt")  # replace with your webpage URL

    def tearDown(self):
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        # Clean up the test by deleting the inserted pet from the database
        query="DELETE FROM adoption_requests WHERE name='John Doe' AND email='john.doe@example.com'"
        cursor.execute(query)
        conn.commit()
        query="DELETE FROM pets where username='rick'"
        cursor.execute(query)
        conn.commit()
        query="DELETE FROM pets where username='rick1'"
        cursor.execute(query)
        conn.commit()
        # discard the remaining result
        cursor.fetchall()
        cursor.close()
        conn.close()
        self.driver.quit()
       

    def test_page_title(self):
        expected_title = "Adopt"
        self.assertEqual(expected_title, self.driver.title)

    def test_nav_links1(self):
        links = [
            {"text": "GO BACK TO HOME", "href": "http://127.0.0.1:5000/main"},
            {"text": "REGISTER PET", "href": "http://127.0.0.1:5000/register"},
            {"text": "CONTACT US", "href": "http://127.0.0.1:5000/adopt#contact"},
            {"text": "SIGN IN", "href": "http://127.0.0.1:5000/signin"},
        ]

        nav_bar = self.driver.find_element(By.CSS_SELECTOR, ".navbar-nav")
        nav_links = nav_bar.find_elements(By.CSS_SELECTOR, "li a")

        for i, link in enumerate(links):
            self.assertEqual(link["text"], nav_links[i].text)
            self.assertEqual(link["href"], nav_links[i].get_attribute("href"))

    def test_count_displayed_on_page(self):
        response = self.app.get('http://127.0.0.1:5000/adopt')
        self.assertEqual(response.status_code, 200)
        count_on_page = int(response.data.decode().split('Showing ')[1].split(' ')[0])
        
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pets")
        count_in_db = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        self.assertEqual(count_on_page, count_in_db)

    def test_fetch_endpoint(self):
        response = self.app.get('/fetch')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<div class="content">', response.data)
        self.assertIn(b'<img src="data:image/png;base64,', response.data)
        self.assertIn(b'<h2 id="pet-name">', response.data)
        self.assertIn(b'<p>Approx age:', response.data)
        self.assertIn(b'<p>Breed:', response.data)
        self.assertIn(b'<p>Location:', response.data)
        self.assertIn(b'<h6>', response.data)
        self.assertIn(b'<button class="adopt-1"', response.data)
    

    def test_get_pet_details(self):
        # create a mock image file
        with open('/Users/aditi/Downloads/Pet-Pawradise-main 2/backend/d.jpeg', 'rb') as f:
            image_data = f.read()
        image = io.BytesIO(image_data)
        image.filename = 'test.jpg'
        # Set up the test by inserting a pet into the database
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pets (username, pet, petname, age_years, age_months, breed, vaccination, state, image, description, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ('rick1', 'cat', 'Whiskers', 2, 6, 'Siamese', True, 'CA', image_data, 'A lovable cat', '123 Main St'))
        conn.commit()

        # Send a GET request to the endpoint for the inserted pet
        query="select id from pets where username='rick1';"
        cursor.execute(query)
        result = cursor.fetchone()
        pet_id = result[0] if result is not None else None 
        print(f"Pet ID: {pet_id}") 
        
        response = self.app.get(f'http://127.0.0.1:5000/pets/{pet_id}')
        # self.assertEqual(response.status_code, 200)

        # Extract the JSON object from the response
        pet = response.json

        # Assert that the pet details in the JSON object are correct
        self.assertEqual(pet['id'], pet_id)
        self.assertEqual(pet['pet'], 'cat')
        self.assertEqual(pet['petname'], 'Whiskers')
        self.assertEqual(pet['age_years'], 2)
        self.assertEqual(pet['age_months'], 6)
        self.assertEqual(pet['breed'], 'Siamese')
        self.assertTrue(pet['vaccination'])
        self.assertEqual(pet['state'], 'CA')
        self.assertEqual(pet['description'], 'A lovable cat')
        self.assertEqual(pet['address'], '123 Main St')

        cursor.close()
        conn.close()

    
    def test_adopt_request_fail(self):
        # define the request data
        data={
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '123-456-7890',
            'address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip': '12345',
            'id': '10000000',
            'experience': 'Yes',
            'message': 'I love this pet!'
        }

        # make the request
        response = self.app.post('/adopt', data=data, follow_redirects=True)

        # assert that the response is successful and contains the success message
        # self.assertEqual(response.status_code, 200)
        self.assertIn(b'ID doesnot exist! Try Again.', response.data)

    def test_adopt_request_successful(self):
        # define the request data
         # create a mock image file
        with open('/Users/aditi/Downloads/Pet-Pawradise-main 2/backend/d.jpeg', 'rb') as f:
            image_data = f.read()
        image = io.BytesIO(image_data)
        image.filename = 'test.jpg'
        # Set up the test by inserting a pet into the database
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pets (username, pet, petname, age_years, age_months, breed, vaccination, state, image, description, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ('rick', 'cat', 'Whiskers', 2, 6, 'Siamese', True, 'CA', image_data, 'A lovable cat', '123 Main St'))
        conn.commit()

        query="select id from pets where username='rick'"
        cursor.execute(query)
        petid = cursor.fetchone()
        print(petid)

        data={
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '123-456-7890',
            'address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip': '12345',
            'id': petid,
            'experience': 'Yes',
            'message': 'I love this pet!'
        }

        # make the request
        response = self.app.post('/adopt', data=data, follow_redirects=True)

        # assert that the response is successful and contains the success message
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Adoption', response.data)

        cursor.close()
        conn.close()




if __name__ == '__main__':
    unittest.main()
