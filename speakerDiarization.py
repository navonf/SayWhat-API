from google.cloud import speech_v1p1beta1 as speech
import os, ssl


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="googleCloud.json"

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

class SpeakerDiarization:
    def __init__(self, speakerCount):
        self.headers = None
        self.url = None
        self.speakerCount = speakerCount

    def speechDiarization(self, audioName):
        speakerCount = 2

        with open(audioName, 'rb') as audio_file:
            content = audio_file.read()
            client = speech.SpeechClient()
            audio = speech.types.RecognitionAudio(content=content)
            config = speech.types.RecognitionConfig(
                encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code='en-US',
                enable_speaker_diarization=True,
                diarization_speaker_count=self.speakerCount)

            print('Waiting for operation to complete...')
            response = client.recognize(config, audio)
            result = response.results[-1]
            words_info = result.alternatives[0].words
            return words_info

    def unifyWords(self, words_info):
        result = ""
        for word in words_info:
            result += word.word +" "
        return result

    def personDialogue(self, words_info):
        result = {}

        for i in range(1, self.speakerCount+1):
            result[i] = []

        for word in words_info:
            result[word.speaker_tag].append(word)

        return result

#
#
# sd = SpeakerDiarization(2)
# result = sd.speechDiarization("Navon_Justin.wav")
# print(sd.unifyWords(result))
# print(sd.personDialogue(result))
