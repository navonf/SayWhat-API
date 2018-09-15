from flask import request, Flask
from time import sleep
from speakerRecognition import SpeakerRecognition
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
