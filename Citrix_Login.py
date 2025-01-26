import csv
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging

#Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#Email configuration
EMAIL_ADDRESS = "******" #Sender email
EMAIL_PASSWORD = "******" #Sender email password
RECIPIENT_EMAIL = "********" #Recipient email

#Citrix Configuration
CITRIX_URL = "https://login.citrix.com/"

def send_email(subject, body):
    """Send email with the given subject and body"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        
        logging.info(f"Email sent successfully to {RECIPIENT_EMAIL}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def automate_login_logout(username, password):
    """Automate login and logout for a given user ID."""
    try:
        Options = Options()
        Options.add_argument("--headless") # Run browser in headless mode
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), Options=Options)

        driver.get(CITRIX_URL)

        # Locate and interact with login fields (adjust the selectors as needed)
        username_fields = driver.find_element(By.NAME, "username")
        password_fields = driver.find_element(By.NAME, "password")

        username_fields.send_keys(username)
        username_fields.send_keys(password)
        password_fields.send_keys(Keys.RETURN)

        logging.info(f"Logged in successfully as {username}.")
        time.sleep(10) # Wait for 10 seconds

        # Perfrom logout adjust the selector as needed
        logout_button = driver.find_element(By.ID, "logoutButton")
        logout_button.click()

        logging.info(f"Logged out successfully for {username}.")
        driver.quit()

        return f"User {username}:- Login and logout successful."
    except Exception as e:
        logging.error(f"Error during login/logout for {username}: {e}")
        return f"User {username}:- Error during login/logout.\n"
    
def main():
    status_reports = []

    # Load user credentials from CSV file
    with open('D:\Python Projects\Citrix login\Citrix_User_Credentials.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)  
        c=1
        for row in reader:
            username = row.get('username')
            password = row.get('password')
            status = automate_login_logout(username, password)
            status_reports.append(str(c)+"."+status)
            c=c+1

    report_body = "\n".join(status_reports)
    send_email("Citrix Login/Logout Status Report", report_body)

if __name__ == "__main__":
    main()

      