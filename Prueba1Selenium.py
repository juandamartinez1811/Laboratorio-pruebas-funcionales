from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

def screenshot_name(prefix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.png"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://the-internet.herokuapp.com/login")
time.sleep(2)

driver.save_screenshot(screenshot_name("01_login_page"))

user_input = driver.find_element(By.ID, "username")
password_input = driver.find_element(By.ID, "password")

user_input.send_keys("tomsmith")
driver.save_screenshot(screenshot_name("01_name_page"))
password_input.send_keys("juan") 
driver.save_screenshot(screenshot_name("01_passw_page"))

login_button = driver.find_element(By.CSS_SELECTOR, "button.radius")
login_button.click()

time.sleep(2)

try:
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success"))
    ).text
    print("Login exitoso:", success_message)
    driver.save_screenshot(screenshot_name("02_login_success"))

except:
    error_message = driver.find_element(By.CSS_SELECTOR, ".flash").text
    print("Login fallido:", error_message)

    driver.save_screenshot(screenshot_name("02_login_failed"))


driver.quit()
