from speakerRecognition import SpeakerRecognition
from speakerDiarization import  SpeakerDiarization
from textAnalytics import TextAnalytics
from pydub import AudioSegment
import time


class TextVoiceParser:

    def __init__(self, dialogues, audioName):
        self.personDialogue = dialogues
        self.audioName = audioName
        self.mapFinal = {}

    def recognizeSpeakers(self):
        for speaker_tag in self.personDialogue:
            self.splitAudio(speaker_tag)

    def splitAudio(self, number):
        audio = AudioSegment.from_file(self.audioName, format="wav")
        personAudio = AudioSegment.empty()
        len(personAudio)

        # How much seconds should I add per word at the end? Adding a second for now
        for dialogue in self.personDialogue[number]:
            if (len(personAudio) >= 30000):
                break
            personAudio += audio[dialogue.start_time.seconds*1000 : dialogue.end_time.seconds*1000]

        file_handle = personAudio.export(str(number)+self.audioName, format="wav")
        self.recognition(str(number)+self.audioName, number)

    def recognition(self, personVoice, number):
        sr = SpeakerRecognition()
        operationid = sr.identify(personVoice, sr.getAllProfile(), True)
        time.sleep(8)
        if (sr.getIdentification(operationid) not in self.mapFinal.values()):
            self.mapFinal[number] = sr.getIdentification(operationid)

# sd = SpeakerDiarization(2)
# ta = TextAnalytics()
# result = sd.speechDiarization("Navon_Justin.wav")
# print(ta.getKeyPhrases(sd.unifyWords(result)))
# tp = TextVoiceParser(sd.personDialogue(result), "Navon_Justin.wav")
# tp.recognizeSpeakers()
# print(tp.mapFinal)
