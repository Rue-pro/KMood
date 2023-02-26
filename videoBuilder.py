import time
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import cv2
import json


class VideoBuilder:
    def __init__(self, assetsPath, projectPath):
        self.projectPath = projectPath
        self.assetsPath = assetsPath
        self.speechPath = os.path.join(projectPath, 'Speech')
        self.speechAudioPath = os.path.join(self.speechPath, 'Audios')
        self.speechVideoPath = os.path.join(self.speechPath, 'Videos')

    def convertVideosToAudios(self):
        videos = os.listdir(self.speechVideoPath)


        for index, video in enumerate(videos):
            if video.find(".mp4") == -1:
                continue

            # number = video[0:2]
            # try:
            #     number = int(number)
            #     if number > 39:
            #         print("do clip", number, video)
            #         videoFileClip = VideoFileClip(os.path.join(self.speechVideoPath, video))
            #         videoFileClip.audio.write_audiofile(os.path.join(self.speechAudioPath, video.replace(".mp4", ".mp3")))
            # except Exception:
            #     number = int(video[0:1])
            #     print(number)
            #     if number > 3 & number < 10:
            #         print("do clip", number, video)
            #         videoFileClip = VideoFileClip(os.path.join(self.speechVideoPath, video))
            #         videoFileClip.audio.write_audiofile(os.path.join(self.speechAudioPath, video.replace(".mp4", ".mp3")))



            videoFileClip = VideoFileClip(os.path.join(self.speechVideoPath, video))
            videoFileClip.audio.write_audiofile(os.path.join(self.speechAudioPath, video.replace(".mp4", ".mp3")))

    def cropAudios(self):
        audios = os.listdir(self.speechAudioPath)

        for index, audio in enumerate(audios):
            if audio.find(".mp3") == -1:
                break

            clip = AudioFileClip(os.path.join(self.speechAudioPath, audio))
            clip = clip.subclip(0, clip.duration - 0.50)
            clip.write_audiofile(os.path.join(self.speechAudioPath, "Cropped", audio))

    def createAudioSchema(self):
        audioSchema = []
        audios = os.listdir(self.speechAudioPath)

        for index, audio in enumerate(audios):
            if audio.find(".mp3") == -1:
                continue

            clip = AudioFileClip(os.path.join(self.speechAudioPath, audio))

            audioInfo = {
                "audio": {
                    "name": audio,
                    "duration": clip.duration
                },
                "video": {
                    "name": "",
                    "start": 0,
                    "end": 0
                }
            }

            audioSchema.append(audioInfo)

        jsonString = json.dumps(audioSchema)
        jsonFile = open(os.path.join(self.projectPath, "schema.json"), "w")
        jsonFile.write(jsonString)
        jsonFile.close()

    def buildVideo(self):
        videos = os.path.join(self.assetsPath, "Videos")
        sentences = json.load(open(os.path.join(self.projectPath, "schema.json")))
        for sentence in sentences:
            if sentence['video']['name'] == "":
                continue
            speechPath = self.speechAudioPath + "/" + sentence['audio']['name']
            slicedVideo = VideoFileClip(videos + "/" + sentence['video']['name'] + ".mp4").subclip(60, 120)
            slicedVideoNoAudio = slicedVideo.without_audio()
            speech = AudioFileClip(speechPath)
            compositeSpeech = CompositeAudioClip([speech])
            slicedVideoNoAudio.audio = compositeSpeech
            slicedVideoNoAudio.write_videofile(self.projectPath + "/Videos/" + sentence['audio']['name'] + ".mp4")
