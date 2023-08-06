import json
import os
import re


def generate_article_config(article_path, map_word_to_change_word, article_config_path):
    print("Generating article config...")

    article = _get_article_from_file(article_path=article_path)
    article_without_unnecessary_chars = _remove_unnecessary_chars_from_article(article)
    article_with_readable_words = _replace_words_to_readable_words(article_without_unnecessary_chars, map_word_to_change_word)
    article_sentences = _create_sentences_arr_from_article(article_with_readable_words)
    article_config = _create_article_config(article_sentences)
    save_article_config(article_config=article_config, article_config_path=article_config_path)


def get_article_config_from_file(article_config_path):
    print("Uploading article from config file...")

    with open(article_config_path, "r") as file:
        article_config = json.loads(file.read())
        file.close()
        return article_config


def get_sentence_file_name(sentence):
    print("Generating file name from sentence...")

    return re.sub('[^A-Za-z0-9]+', '', sentence)[0:100]


def _get_article_from_file(article_path):
    print("Uploading article from file...")

    with open(article_path, "r") as file:
        article = file.read()
        file.close()
        if article == "":
            raise Exception("Article is empty!")
        return article


def _remove_unnecessary_chars_from_article(article):
    print("Removing unnecessary characters from article...")

    notion_double_quotes_end = "вЂќ"
    return article.replace('"', "").replace("’", "").replace("\n", "") \
        .replace(notion_double_quotes_end, "").replace("вЂ™", "").replace("Ђќ", "")


def _replace_words_to_readable_words(article, map_word_to_change_word):
    print("Replacing all words to readable words...")

    article_with_replaced_words = article
    for word in map_word_to_change_word:
        article_with_replaced_words = article_with_replaced_words.replace(word, map_word_to_change_word[word])
    return article_with_replaced_words


def _create_sentences_arr_from_article(article):
    print("Creating sentences array from article...")

    divided_article = [article]
    division_chars = [".", "?", ";", "!"]

    for division_char in division_chars:
        new_divided_article = []
        for sentence in divided_article:
            splitted_sentences = sentence.split(division_char)
            for index, splitted_sentence in enumerate(splitted_sentences):
                if index != len(splitted_sentences) - 1:
                    new_splitted_sentence = splitted_sentence + division_char
                else:
                    new_splitted_sentence = splitted_sentence

                if new_splitted_sentence != "":
                    new_divided_article.append(new_splitted_sentence)
        divided_article = new_divided_article

    return divided_article


def _create_article_config(article_sentences):
    print("Creating article config...")

    article_config = []

    for sentence in article_sentences:
        article_config.append({
            "text": sentence,
            "record": None,
        })

    return article_config


def save_article_config(article_config, article_config_path):
    print("Saving article config...")

    jsonFile = open(os.path.join(article_config_path), "w")
    jsonFile.write(json.dumps(article_config, indent=2))
    jsonFile.close()
