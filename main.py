import json
import os

from generateArticleConfig import generate_article_config, fix_article_config
from makeAudio import make_audio

KMOOD_PROJECT = "C:/Dev/YouTubeAutomation/KMood/ATEEZ_Yunho"
KMOOD_PROJECT_AUDIOS_PATH = os.path.join(KMOOD_PROJECT, "audios")
KMOOD_PROJECT_ARTICLE = os.path.join(KMOOD_PROJECT, "article.txt")
KMOOD_PROJECT_ARTICLE_CHANGES = os.path.join(KMOOD_PROJECT, "article_changes.json")
KMOOD_PROJECT_ARTICLE_CONFIG_PATH = os.path.join(KMOOD_PROJECT, "article_config.json")


def prepare_project():
    print("Prepare project...")
    isExist = os.path.exists(KMOOD_PROJECT)
    if isExist:
        print("KMOOD_PROJECT is already existing!")
    else:
        os.makedirs(KMOOD_PROJECT_AUDIOS_PATH)
        print("KMOOD_PROJECT is created!")

    isExist = os.path.exists(KMOOD_PROJECT_AUDIOS_PATH)
    if isExist:
        print("KMOOD_PROJECT_AUDIOS_PATH is already existing!")
    else:
        os.makedirs(KMOOD_PROJECT_AUDIOS_PATH)
        print("KMOOD_PROJECT_AUDIOS_PATH is created!")

    isExist = os.path.isfile(KMOOD_PROJECT_ARTICLE)
    if isExist:
        print("KMOOD_PROJECT_ARTICLE is exist!")
    else:
        raise Exception("KMOOD_PROJECT_ARTICLE not exist! Given path: " + KMOOD_PROJECT_ARTICLE)

    isExist = os.path.isfile(KMOOD_PROJECT_ARTICLE_CHANGES)
    if isExist:
        print("KMOOD_PROJECT_ARTICLE_CHANGES is exist!")
    else:
        raise Exception("KMOOD_PROJECT_ARTICLE_CHANGES not exist! Given path: " + KMOOD_PROJECT_ARTICLE_CHANGES)


def get_article_changes():
    print("Uploading article changes from config file...")

    with open(KMOOD_PROJECT_ARTICLE_CHANGES, "r") as file:
        article_changes = json.loads(file.read())
        file.close()
        return article_changes


if __name__ == "__main__":
    do_config_fix = False
    do_make_audio = not do_config_fix & True

    prepare_project()

    if do_make_audio is True:
        make_audio(article_config_path=KMOOD_PROJECT_ARTICLE_CONFIG_PATH, audios_path=KMOOD_PROJECT_AUDIOS_PATH)
        exit()

    article_changes = get_article_changes()

    if do_config_fix:
        fix_article_config(article_path=KMOOD_PROJECT_ARTICLE, map_word_to_change_word=article_changes,
                           article_config_path=KMOOD_PROJECT_ARTICLE_CONFIG_PATH)
    else:
        generate_article_config(article_path=KMOOD_PROJECT_ARTICLE, map_word_to_change_word=article_changes,
                                article_config_path=KMOOD_PROJECT_ARTICLE_CONFIG_PATH)

    print("Article config generated successfully, check it out and start generating audios from this config!")
