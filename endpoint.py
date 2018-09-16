from flask import request, Flask
from time import sleep
from speakerRecognition import SpeakerRecognition
from speakerDiarization import SpeakerDiarization
from textAnalytics import TextAnalytics
from textVoiceParser import TextVoiceParser
import os
#  Just in case if we get the CORs error in the client
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['POST',])
def register():
    data = dict(request.form)
    file = request.files.get('voice')
    if file is None:
        print('No selected file')
        return "bad"

    filename = file.filename
    file.save(os.path.join(os.path.dirname(__file__), filename))
    sr = SpeakerRecognition()
    name = filename.split(".")[0]
    sr.toWAV(filename, name + ".wav")
    sr.Enroll(sr.CreateProfile(), name + ".wav")
    sleep(5)
    return "good"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

@app.route('/analyze', methods=['POST',])
def analyzeVoice():
    data = int(request.form.get('speakers')[0])
    file = request.files.get('voice')
    if file is None:
        print('No selected file')
        return "bad"

    filename = file.filename
    file.save(os.path.join(os.path.dirname(__file__), filename))
    name = filename.split(".")[0]
    sr = SpeakerRecognition()
    sr.toWAV(filename, name + ".wav")
    filename = name + ".wav"
    sr.toMono(filename)
    sd = SpeakerDiarization(data)
    ta = TextAnalytics()
    result = sd.speechDiarization(filename)
    keywords = ta.getKeyPhrases(sd.unifyWords(result))
    tp = TextVoiceParser(sd.personDialogue(result), filename)
    tp.recognizeSpeakers()
    mapFinal = tp.mapFinal
    print(keywords)
    print(mapFinal)

    return "good"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
