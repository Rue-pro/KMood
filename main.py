import logging
import time
import json
import os

from obs import OBSRemote
from speechToText import SpeechToText
from videoBuilder import VideoBuilder
from redditParser import RedditParser
from redditVideoBuilder import RedditVideoBuilder

logging.basicConfig(level=logging.INFO)

CONFIG = {
    "rootPath": "C:/Dev/YouTube Automation/",
    "recordedVideos": "C:/Users/Alina/Videos",
}

KMOOD_CONFIG = {
    "path": os.path.join(CONFIG["rootPath"], "KMood"),
    "assets": os.path.join(CONFIG["rootPath"], "KMood", "Assets"),
    "scenario": os.path.join(CONFIG["rootPath"], "KMood", "NewJeans_Hanni", "article.txt"),
    "scenarioTextChanges": os.path.join(CONFIG["rootPath"], "KMood", "NewJeans_Hanni", "changes.json"),
    "project": os.path.join(CONFIG["rootPath"], "KMood", "NewJeans_Hanni")
}

REDDIT_CONFIG = {
    "path": os.path.join(CONFIG["rootPath"], "Reddit"),
    "project": os.path.join(CONFIG["rootPath"], "Reddit", "what_do_you_enjoy_more_the_older_you_get"),
    "urlToParse": "/110qy0d/what_do_you_enjoy_more_the_older_you_get/"
}


def renameFiles():
    path = 'C:/Dev/YouTube Automation/KMood/NewJeans_Hanni/Speech/Audios'

    files = os.listdir(path)

    for index, file in enumerate(files):
        os.rename(os.path.join(path, file), os.path.join(path, file[0:100]), ".mp4")


def moveAndRenameRecord(newName):
    path = CONFIG["recordedVideos"]

    videos = os.listdir(path)

    for video in videos:
        if video[0:4] == "2023":
            newName = newName.replace("?", "")
            os.rename(path + "/" + video, KMOOD_CONFIG["project"] + "/Speech/Videos/" + newName[0:100] + ".mp4")


def prepareKMood():
    print("Prepare content for KMood project...")

    CHANGES_FILE = open(KMOOD_CONFIG["scenarioTextChanges"])
    CHANGES = json.load(CHANGES_FILE)

    videoBuilder = VideoBuilder(KMOOD_CONFIG["assets"], KMOOD_CONFIG["project"])

    with open(KMOOD_CONFIG["scenario"], "r") as file:
        content = file.read().replace("\n", "")
        sentences = content.replace('"', "").replace("’", "").replace("вЂ™", "").replace("Ђќ", "").split(".")

    obs = OBSRemote()
    speechToText = SpeechToText()
    speechToText.checkCaptcha()

    for index, _sentence in enumerate(sentences):
        sentence = _sentence
        for word in CHANGES:
            sentence = sentence.replace(word, CHANGES[word])

        time.sleep(3)
        if sentence:
            print("SENTENCE", sentence)
            speechToText.preRecord(sentence)
            try:
                print("DO RECORD")

                obs.disableMic()
                obs.startRecording()
                speechToText.doPlayRecorded()
            except KeyboardInterrupt:
                pass

            print("STOP RECORD")
            obs.stopRecording()
            obs.enableMic()

            time.sleep(3)
            moveAndRenameRecord(str(index) + "." + _sentence)

    obs.disconnect()
    speechToText.disconnect()

    videoBuilder.convertVideosToAudios()
    videoBuilder.cropAudios()
    print("Content prepared for KMood project...")


def prepareReddit():
    print("Prepare content for Reddit project...")
    if not os.path.isdir(REDDIT_CONFIG['project']):
        os.makedirs(REDDIT_CONFIG['project'])

    redditParser = RedditParser(REDDIT_CONFIG['project'], REDDIT_CONFIG["urlToParse"])
    print("Content prepared for Reddit project...")


if __name__ == "__main__":
    redditVideoBuilder = RedditVideoBuilder()
    redditVideoBuilder.build()
    # prepareKMood()