import time
import keyboard
import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

INITIAL_TEXT = "This is first sentence to check."


class SpeechToText:
    url = "https://www.gstatic.com/cloud-site-ux/text_to_speech/text_to_speech.min.html"
    downloadedRequests = []

    def __init__(self):
        print("Opening browser and setting up text to speech...")

        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=caps)
        self.driver.get(self.url)
        time.sleep(5)

        # Locate the app
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
        print("Checking captcha...")

        self._writeToTextarea(INITIAL_TEXT)
        self._submit()
        time.sleep(5)
        if self.driver.find_element(By.CSS_SELECTOR, 'div#container'):
            print("Captcha appeared, handle it accordingly")

            keyboard.wait("enter")
        self._waitRecordFinished()

    def preRecord(self, sentence):
        print("Pasting sentence:" + sentence + "...")
        self._writeToTextarea(sentence)
        self._submit()
        self._waitRecordFinished()

    def getResponse(self, audio_file_name):
        print("Getting binary audio data from browser logs...")

        def process_browser_log_entry(entry):
            response = json.loads(entry['message'])['message']
            return response

        browser_log = self.driver.get_log('performance')
        events = [process_browser_log_entry(entry) for entry in browser_log]

        content = ""
        for event in events:
            if "requestId" not in event["params"]:
                continue

            requestId = event["params"]["requestId"]

            if requestId in self.downloadedRequests:
                continue

            try:
                body = self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
                try:
                    content = json.loads(body['body'])['audioContent']
                except Exception:
                    pass
            except Exception:
                pass

        self.downloadedRequests.append(requestId)

        if content == "":
            Exception("Could not get audio content for audio:", audio_file_name)
        return content

    def disconnect(self):
        self.driver.close()
