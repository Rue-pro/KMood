import os.path
import time
import keyboard
import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class RedditParser:
    url = "https://www.reddit.com/r/AskReddit/comments"

    def __init__(self, projectPath, thread):
        self.projectPath = projectPath
        self.driver = webdriver.Chrome()
        self.driver.get(self.url + thread)
        time.sleep(5)
        self._parse_comments()

    def _parse_comments(self):
        comments = self.driver.find_elements(By.CLASS_NAME, "Comment")
        time.sleep(5)
        tree = []
        for comment in comments[0:5]:
            commentHeader = comment.find_element(By.CSS_SELECTOR, "div[data-testid=post-comment-header]").find_element(
                By.XPATH, "..")
            level = commentHeader.find_element(By.CSS_SELECTOR, "span").text
            author = comment.find_element(By.CSS_SELECTOR, "a[data-testid=comment_author_link]").text
            timestamp = comment.find_element(By.CSS_SELECTOR, "a[data-testid=comment_timestamp]").text
            rating = comment.find_element(By.CSS_SELECTOR, "button[data-click-id=upvote]+div").text
            try:
                content = comment.find_element(By.CSS_SELECTOR, "div[data-testid=comment]").text

            except Exception:
                print(Exception)

            time.sleep(5)

            print(author)

            jsonComment = {
                "level": level,
                "author": author,
                "timestamp": timestamp,
                "content": content,
                "rating": rating,
                "replies": []
            }

            for index in range(int(level[6:len(level)])):
                print("index", index)
                print("tree", tree, len(tree))
                if index == 0:
                    targetComment = tree
                else:
                    targetComment = tree[len(tree) - 1]["replies"]

            targetComment.append(jsonComment)



        jsonString = json.dumps(tree)
        jsonFile = open(os.path.join(self.projectPath, "comments.json"), "w")
        jsonFile.write(jsonString)
        jsonFile.close()
