import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pygame import mixer

# List of URLs
urls = [
    "https://www.popmart.com/my/products/659/CRYBABY-Sad-Club-Series-Silicone-Plush-Earphone-Bag",
    "https://www.popmart.com/my/products/661/CRYBABY-Sad-Club-Series-Plush-Figure",
    "https://www.popmart.com/my/products/1385/CRYBABY-Crying-Again-Series-Earphone-Case", # love make us cry
]

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def accept_terms(driver):
    accept_tnc = driver.find_element(By.CLASS_NAME, 'policy_acceptBtn__ZNU71')
    if accept_tnc.text == "ACCEPT":
        accept_tnc.click()
        print("T&C accepted")
    else:
        print('no T&C')

def login(driver):
    try:
        # Click on Sign in
        login = driver.find_element(By.XPATH, "//*[contains(text(), 'Sign in')]")
        login.click()
        # Wait for the login form to appear
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'SIGN IN OR REGISTER')]")))
        # Fill in the email
        email = driver.find_element(By.XPATH, '//*[@id="email"]')
        email.send_keys('#REDACTED')
        # Click on continue
        continueBtn = driver.find_element(By.XPATH, "//*[contains(text(), 'CONTINUE')]")
        continueBtn.click()
        # Wait for the password field to appear
        WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
        password = driver.find_element(By.XPATH, '//*[@id="password"]')
        password.send_keys('#REDACTED')
        # Click on Sign in
        signInBtn = driver.find_element(By.XPATH,'//button[normalize-space()="SIGN IN"]')
        signInBtn.click()
        time.sleep(10)
        selected_url = random.choice(urls)
        driver.get(selected_url)

    except Exception as error:
        print('login failed')
        print(error)
        exit()

def play_sound():
    mixer.init()
    mixer.music.load("bell.wav")
    mixer.music.play(100)
    print("🎉 🎉 🎉")
    while mixer.music.get_busy():
        time.sleep(300)

def check_availability(driver):
    try:
        driver.find_element(By.XPATH, "//*[contains(text(), 'BUY NOW')]")
        return True
    except:
        return False

def buy_now(driver):
    try:
        buy_now = driver.find_element(By.XPATH, "//*[contains(text(), 'BUY NOW')]")
        buy_now.click()
        WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'PROCEED TO PAY')]")))
        time.sleep(5)
        proceed_to_pay = driver.find_element(By.XPATH, "//*[contains(text(), 'PROCEED TO PAY')]")
        proceed_to_pay.click()
        play_sound()
    except Exception as error:
        print(error)
        print('Buy now failed')
        exit()


def main():
    driver = initialize_driver()
    selected_url = random.choice(urls)
    driver.get(selected_url)

    accept_terms(driver)
    login(driver)

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Details')]")))

    found = False
    while not found:
        time.sleep(random.randrange(10,20))
        selected_url = random.choice(urls)
        driver.get(selected_url)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Details')]")))
        if check_availability(driver):
            found = True
            break
        else:
            print("Not available")

    buy_now(driver)

if __name__ == "__main__":
    main()