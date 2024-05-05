import speech_recognition as sr
from flask import Flask, request

app = Flask(__name__)

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    transcript = ""

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        
        try:
            transcript = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            transcript = "Could not understand the audio"
        except sr.RequestError as e:
            transcript = f"Error: {e}"
    
    return transcript

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return 'No file provided'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    try:
        transcript = transcribe_audio(file)
        return transcript
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
