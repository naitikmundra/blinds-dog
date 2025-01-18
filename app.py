import os
from flask import Flask, request, render_template
import speech_recognition as sr
from pydub import AudioSegment
import subprocess

app = Flask(__name__)

# Function to convert speech to text
def convert_speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text
    except Exception as e:
        return f"Error: {str(e)}"
@app.route("/")
def index():
    
    convt_text= None
    return render_template("index.html", convt_text=convt_text)
# Route to handle the form and convert speech
@app.route("/getspeech", methods=["GET", "POST"])
def speech():

    if request.method == "POST":
        if "audio_file" in request.files:


            audio_file = request.files["audio_file"]
            temp_filename = "file.mp3"
            audio_file.save(temp_filename)
            sound = AudioSegment.from_mp3("file.mp3")
            sound.export("file.wav", format="wav")
            # Save the audio file temporarily


            # Convert the audio file to text
            convt_text = convert_speech_to_text(temp_filename)

            # Remove the temporary file after processing
            os.remove(temp_filename)
    
    return render_template("index.html", convt_text=convt_text)

if __name__ == "__main__":
    app.run(debug=True)
