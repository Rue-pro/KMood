from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import numpy as np

data = [
    {
        "level": "level 1",
        "author": "tbama11",
        "timestamp": "5 days ago",
        "contentArr": [
            {
                "text": "Huening Kai is a multitalented artist and member of the popular K-Pop group TXT",
                "record":
                    "0.Huening Kai is a multitalented artist and member of the popular K-Pop group TXT",
                "duration": "00:00:07",
            },
            {
                "text": "He was born on August 14, 2002, in Hawaii",
                "record": "1. He was born on August 14, 2002, in Hawaii",
                "duration": "00:00:04",
            },
            {
                "text": "Kai's passion for music started at a young age",
                "record": "2. Kai's passion for music started at a young age",
                "duration": "00:00:03",
            },
            {
                "text": "Growing up, he lived in many different countries, including Brazil, Germany, and China, which gave him a unique perspective on the world and influenced his artistry",
                "record":
                    "3. Growing up, he lived in many different countries, including Brazil, Germany, and China, which gave him a unique perspective on the world and influenced his artistry",
                "duration": "00:00:11",
            },
            {
                "text": "Today, he is known for his powerful vocals, impressive musicianship, and charming personality, which have made him a beloved member of the K-Pop community",
                "record":
                    "4. Today, he is known for his powerful vocals, impressive musicianship, and charming personality, which have made him a beloved member of the K-Pop community",
                "duration": "00:00:10",
            },
            {
                "text": "Today we'll take a closer look at Huening Kai's life, career, and achievements",
                "record":
                    "5. Today we'll take a closer look at Huening Kai's life, career, and achievements",
                "duration": "00:00:05",
            },
            {
                "text": "But before we start, don't forget to like and subscribe to support our channel",
                "record":
                    "6. But before we start, don't forget to like and subscribe to support our channel",
                "duration": "00:00:05",
            },
            {
                "text": "Kai's net worth is estimated at $2,000,000",
                "record": "7.Kai's net worth is estimated at $2,000,000",
                "duration": "00:00:04",
            },
            {
                "text": "Huening Kai is a multitalented artist and member of the popular K-Pop group TXT",
                "record":
                    "0.Huening Kai is a multitalented artist and member of the popular K-Pop group TXT",
                "duration": "00:00:07",
            },
            {
                "text": "He was born on August 14, 2002, in Hawaii",
                "record": "1. He was born on August 14, 2002, in Hawaii",
                "duration": "00:00:04",
            },
            {
                "text": "Kai's passion for music started at a young age",
                "record": "2. Kai's passion for music started at a young age",
                "duration": "00:00:03",
            },
            {
                "text": "Growing up, he lived in many different countries, including Brazil, Germany, and China, which gave him a unique perspective on the world and influenced his artistry",
                "record":
                    "3. Growing up, he lived in many different countries, including Brazil, Germany, and China, which gave him a unique perspective on the world and influenced his artistry",
                "duration": "00:00:11",
            },
            {
                "text": "Today, he is known for his powerful vocals, impressive musicianship, and charming personality, which have made him a beloved member of the K-Pop community",
                "record":
                    "4. Today, he is known for his powerful vocals, impressive musicianship, and charming personality, which have made him a beloved member of the K-Pop community",
                "duration": "00:00:10",
            },
            {
                "text": "Today we'll take a closer look at Huening Kai's life, career, and achievements",
                "record":
                    "5. Today we'll take a closer look at Huening Kai's life, career, and achievements",
                "duration": "00:00:05",
            },
            {
                "text": "But before we start, don't forget to like and subscribe to support our channel",
                "record":
                    "6. But before we start, don't forget to like and subscribe to support our channel",
                "duration": "00:00:05",
            },
            {
                "text": "Kai's net worth is estimated at $2,000,000",
                "record": "7.Kai's net worth is estimated at $2,000,000",
                "duration": "00:00:04",
            },
        ],
        "rating": "631",
    },
];

videoBorder = 50
videoWidth = 1920
videoHeight = 1080

lastItemPosition = videoBorder

class RedditVideoBuilder:

    def __init__(self):
        self.lastItemPosition = videoBorder

    def _addAuthorAndTimeStamp(self, author, timestamp):
        gap = videoBorder

        author_clip = TextClip(author, fontsize=30, font="IBM Plex Sans-Bold", color='rgb(26, 26, 27)')
        author_clip = author_clip.set_pos((gap, self.lastItemPosition))
        author_clip = author_clip.set_duration(10)
        print("authorClip.size", author_clip.size)

        gap += author_clip.size[0] + 16

        timestamp_clip = TextClip(timestamp, fontsize=30, font="Noto Sans", color='rgb(124, 124, 124)')
        timestamp_clip = timestamp_clip.set_pos((gap, self.lastItemPosition))
        timestamp_clip = timestamp_clip.set_duration(10)
        print("timestamp_clip.size", timestamp_clip.size)

        self.lastItemPosition += author_clip.size[1]

        print("lastItemPosition", self.lastItemPosition)

        return author_clip, timestamp_clip

    def _addComment(self):
        text = "This is a paragraph.\nIt has multiple sentences.\nEach sentence is revealed one by one."

        # Split the text into sentences
        sentences = text.split('\n')

        # Set the font, size, and color for the text
        font = 'Arial'
        fontsize = 30
        color = 'white'

        # Calculate the width and height of the final clip
        total_height = 0
        for sentence in sentences:
            sentence_clip = TextClip(sentence, font=font, fontsize=fontsize, color=color)
            max_width = max(videoWidth, sentence_clip.w)
            total_height += sentence_clip.h

        # Create the final clip with a black background
        background_color = 'black'
        final_clip = ColorClip((videoWidth, videoHeight), (255, 255, 255), duration=60)

        # Add each sentence to the final clip one by one
        y_pos = 0
        for sentence in sentences:
            sentence_clip = TextClip(sentence, font=font, fontsize=fontsize, color=color)
            final_clip = CompositeVideoClip([final_clip, sentence_clip.set_pos(('center', y_pos))])
            y_pos += sentence_clip.h

        # Set the duration of the final clip to be the length of the text
        duration = 5
        final_clip = final_clip.set_duration(duration)

        # Export the final clip as an mp4 file
        final_clip.write_videofile("revealing_sentences.mp4", fps=25)


    def build(self):
        print("do build")
        clip = ColorClip((videoWidth, videoHeight), (255, 255, 255), duration=60)

        # [authorClip, timestampClip] = self._addAuthorAndTimeStamp("tbama11", "5 days ago")
        self._addComment()
        # video = CompositeVideoClip([clip, authorClip, timestampClip])
        # video.write_videofile("redditVideoBuilder.mp4", fps=25)

