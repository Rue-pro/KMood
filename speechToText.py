import time
import keyboard

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

INITIAL_TEXT = "This is first sentence to check."


class SpeechToText:
    url = "https://www.gstatic.com/cloud-site-ux/text_to_speech/text_to_speech.min.html"

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        time.sleep(5)

        # Locate the appW
        self.app_root = self.driver.find_element(By.TAG_NAME, 'ts-app').shadow_root

        # Change to SSML
        radio_host = self.app_root.find_element(By.CSS_SELECTOR, 'ts-input-type-toggle')
        radio_host.click()

        # Save submit button
        self.submit_button = self.driver.find_element(By.TAG_NAME, 'ts-app').shadow_root.find_element(By.ID,
                                                                                                      'button').shadow_root.find_element(
            By.CSS_SELECTOR, 'paper-button')

    def _writeToTextarea(self, sentence):
        textarea_host = self.app_root.find_element(By.CSS_SELECTOR, 'paper-textarea')
        textarea_host.send_keys(Keys.CONTROL + "a")
        textarea_host.send_keys(Keys.DELETE)
        textarea_host.send_keys("<speak>" + sentence + "</speak>")

    def _submit(self):
        self.submit_button.click()

    def _waitRecordFinished(self):
        wait = WebDriverWait(self.driver, 100)
        wait.until(lambda d: 'state-finished' in self.submit_button.get_attribute('class'))

    def checkCaptcha(self):
        self._writeToTextarea(INITIAL_TEXT)
        self._submit()
        time.sleep(5)
        if self.driver.find_element(By.CSS_SELECTOR, 'div#container'):
            # Handle the captcha
            print("Captcha appeared, handle it accordingly")
            keyboard.wait("enter")
        self._waitRecordFinished()

    def preRecord(self, sentence):
        self._writeToTextarea(sentence)
        self._submit()
        self._waitRecordFinished()

    def doPlayRecorded(self):
        self._submit()
        self._waitRecordFinished()

    def disconnect(self):
        self.driver.close()
