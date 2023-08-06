from generateArticleConfig import get_article_config_from_file, get_sentence_file_name, \
    save_article_config
import base64
from speechToText import SpeechToText
import time
import os


def generate_audio_from_binary(binary_audio, audio_path):
    decoded_data = base64.b64decode(binary_audio)
    with open(audio_path, 'wb') as f:
        f.write(decoded_data)


def has_audios_to_generate(audio_config):
    for sentence in audio_config:
        if sentence["record"] is None:
            return True

    return False


def make_audio(article_config_path, audios_path):
    article_config = get_article_config_from_file(article_config_path=article_config_path)

    if not has_audios_to_generate(audio_config=article_config):
        print("No audios to generate!")
        exit()

    speechToText = SpeechToText()
    speechToText.checkCaptcha()

    for index, sentence in enumerate(article_config):
        if sentence["record"] is not None:
            continue

        time.sleep(3)
        audio_file_name = str(index) + " " + get_sentence_file_name(sentence["text"]) + ".wav"

        speechToText.preRecord(sentence["text"])
        binary_audio = speechToText.getResponse(audio_file_name)

        generate_audio_from_binary(binary_audio, os.path.join(audios_path, audio_file_name))

        sentence["record"] = audio_file_name

        save_article_config(article_config=article_config, article_config_path=article_config_path)

    speechToText.disconnect()

    print("Audio files generated successfully, check it out and start editing video!")
