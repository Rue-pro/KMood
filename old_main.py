import logging
import time
import keyboard

logging.basicConfig(level=logging.INFO)

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from obs import OBSRemote

PROJECT_PATH = "C:/Dev/YouTube Automation/KMood/NewJeans_Danielle/"
SCENARIO = PROJECT_PATH + "/article.txt"

def renameFiles():
    path = 'C:/Dev/YouTube Automation/SmoothAI/Image Sequence'

    files = os.listdir(path)

    for index, file in enumerate(files):
        os.rename(os.path.join(path, file), os.path.join(path, file[7:]))



def init():
    sentences = []

    with open(SCENARIO, "r") as file:
        content = file.read()
        sentences = content.replace("\n", "").replace("Danielle's", "<sub alias='DanYELS'>DDD</sub>").replace("Daniel's", "<sub alias='DanYELS'>DDD</sub>").replace("Danielle", "<sub alias='DanYEL'>DDD</sub>").replace("Daniel", "<sub alias='DanYEL'>DDD</sub>").replace("Hyein", "<sub alias='Heyin'>HHH</sub>").replace("HYBE", "<sub alias='Hibe'>HHH</sub>").replace('"', "").split(".")

    print(sentences)

    obs = OBSRemote()

    driver = webdriver.Chrome()
    driver.get("https://www.gstatic.com/cloud-site-ux/text_to_speech/text_to_speech.min.html")
    time.sleep(5)

    # Locate the text area and insert the text
    app_host = driver.find_element(By.TAG_NAME, 'ts-app')
    app_root = app_host.shadow_root

    # Change to SSML
    radio_host = app_root.find_element(By.CSS_SELECTOR, 'ts-input-type-toggle')
    radio_host.click()


    def doRecordSentenceWithCaptcha(sentence):
        textarea_host = app_root.find_element(By.CSS_SELECTOR, 'paper-textarea')
        textarea_host.send_keys(Keys.CONTROL + "a")
        textarea_host.send_keys(Keys.DELETE)
        textarea_host.send_keys("<speak>This is first sentence to check.This is first sentence to check.This is first sentence to check.</speak>")

        button = driver.find_element(By.TAG_NAME, 'ts-app').shadow_root.find_element(By.ID,
                                                                                     'button').shadow_root.find_element(
            By.CSS_SELECTOR, 'paper-button')
        button.click()
        time.sleep(5)

        if driver.find_element(By.CSS_SELECTOR, 'div#container'):
            # Handle the captcha
            print("Captcha appeared, handle it accordingly")
            keyboard.wait("enter")

            # state-loading
            # state-playing
            # state-finished

        wait = WebDriverWait(driver, 100)
        wait.until(lambda d: 'state-finished' in button.get_attribute('class'))

        try:
            print("DO RECORD")

            obs.disableMic()
            obs.startRecording()

            button = driver.find_element(By.TAG_NAME, 'ts-app').shadow_root.find_element(By.ID,
                                                                                         'button').shadow_root.find_element(
                By.CSS_SELECTOR, 'paper-button')
            button.click()

        except KeyboardInterrupt:
            pass

        wait = WebDriverWait(driver, 100)
        wait.until(lambda d: 'state-finished' in button.get_attribute('class'))

        print("STOP RECORD")
        obs.stopRecording()
        obs.enableMic()

    def doRecordSentence(sentence):
        textarea_host = app_root.find_element(By.CSS_SELECTOR, 'paper-textarea')
        textarea_host.send_keys(Keys.CONTROL + "a")
        textarea_host.send_keys(Keys.DELETE)
        textarea_host.send_keys("<speak>" + sentence + "</speak>")

        button = driver.find_element(By.TAG_NAME, 'ts-app').shadow_root.find_element(By.ID,
                                                                                     'button').shadow_root.find_element(
            By.CSS_SELECTOR, 'paper-button')
        button.click()

        wait = WebDriverWait(driver, 100)
        wait.until(lambda d: 'state-finished' in button.get_attribute('class'))

        try:
            print("DO RECORD")

            obs.disableMic()
            obs.startRecording()

            button = driver.find_element(By.TAG_NAME, 'ts-app').shadow_root.find_element(By.ID,
                                                                                         'button').shadow_root.find_element(
                By.CSS_SELECTOR, 'paper-button')
            button.click()

        except KeyboardInterrupt:
            pass

        wait = WebDriverWait(driver, 100)
        wait.until(lambda d: 'state-finished' in button.get_attribute('class'))

        print("STOP RECORD")
        obs.stopRecording()
        obs.enableMic()

    doRecordSentenceWithCaptcha(sentences[0])

    for sentence in sentences:
        time.sleep(3)
        if sentence:
            print("SENTENCE")
            doRecordSentence(sentence)

    obs.disconnect()

    # Close the browser
    driver.close()


if __name__ == "__main__":
    init()
