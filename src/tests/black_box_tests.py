import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
class BlackBoxTestCase(unittest.TestCase): 
    def setUp(self):
        import os
        os.environ["TESTING"] = "1"
        from app import create_app, db
        self.app = create_app()
        with self.app.app_context():
            db.create_all()
        import psycopg2
        conn = psycopg2.connect("dbname=cyber_events user=postgres password=135791")
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE email = %s", ("blackboxtest@example.com",))
        conn.commit()
        cur.close()
        conn.close()
        self.browser = webdriver.Chrome()
        self.browser.get('http://localhost:5001/')
    def test_signup_and_api_key_display(self):
        self.browser.get('http://localhost:5001/users/signup')
        email_input = self.browser.find_element(By.NAME, 'email')
        name_input = self.browser.find_element(By.NAME, 'name')
        submit_button = self.browser.find_element(By.NAME, 'submit')
        test_email = "blackboxtest@example.com"
        test_name = "BlackBox Tester"
        email_input.clear()
        email_input.send_keys(test_email)
        name_input.clear()
        name_input.send_keys(test_name)
        submit_button.click()
        sleep(1)
        body_text = self.browser.find_element(By.TAG_NAME, 'body').text
        print("DEBUG BODY TEXT:")
        print(body_text)
        self.assertIn("Your API key is:", body_text)
        self.assertIn("only time you will see it", body_text)   
if __name__ == '__main__':
    unittest.main()
