import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pygame import mixer

# List of URLs
urls = [
    "https://www.popmart.com/my/products/659/CRYBABY-Sad-Club-Series-Silicone-Plush-Earphone-Bag",
    "https://www.popmart.com/my/products/661/CRYBABY-Sad-Club-Series-Plush-Figure",
    "https://www.popmart.com/my/products/1385/CRYBABY-Crying-Again-Series-Earphone-Case",
    "https://www.popmart.com/my/products/1524/CRYBABY-Crying-Again-Series-Vinyl-Face-Plush-Blind-Box",
    "https://www.popmart.com/my/products/887/CRYBABY-%C3%97-Powerpuff-Girls-Series-Vinyl-Face-Plush-Blind-Box"
]

def initialize_driver():
    driver = webdriver.Chrome()
    return driver

def accept_terms(driver):
    accept_tnc = driver.find_element(By.CLASS_NAME, 'policy_acceptBtn__ZNU71')
    if accept_tnc.text == "ACCEPT":
        accept_tnc.click()
        print("T&C accepted")
    else:
        exit()

def play_sound():
    mixer.init()
    mixer.music.load("bell.wav")
    mixer.music.play(10)
    print("🎉 🎉 🎉")
    while mixer.music.get_busy():
        time.sleep(20)

def check_availability(driver):
    try:
        driver.find_element(By.XPATH, "//*[contains(text(), 'BUY NOW')]")
        return True
    except:
        return False

def main():
    driver = initialize_driver()
    selected_url = random.choice(urls)
    driver.get(selected_url)

    accept_terms(driver)

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Details')]")))

    try:
        driver.find_element(By.XPATH, "//*[contains(text(), 'NOTIFY ME WHEN AVAILABLE')]")
    except:
        play_sound()
        exit()

    found = False
    while not found:
        time.sleep(300)
        selected_url = random.choice(urls)
        driver.get(selected_url)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Details')]")))
        if check_availability(driver):
            found = True
            break
        else:
            print("Not available")

    play_sound()

if __name__ == "__main__":
    main()