import sys

sys.path.append('../')
from obswebsocket import obsws, events, requests


class OBSRemote:
    host = "localhost"
    port = 4444
    password = "secret"
    mic = "Микр./доп."

    def __init__(self):
        self.client = obsws(self.host, self.port, self.password)
        self.client.register(self.on_event)
        self.client.connect()

    @staticmethod
    def on_event(message):
        print(u"Got message: {}".format(message))

    def disconnect(self):
        self.client.disconnect()

    def disableMic(self):
        self.client.call(requests.SetMute(self.mic, True))

    def enableMic(self):
        self.client.call(requests.SetMute(self.mic, False))

    def startRecording(self):
        self.client.call(requests.StartRecording())

    def stopRecording(self):
        self.client.call(requests.StopRecording())