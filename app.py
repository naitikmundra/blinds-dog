import os
from flask import Flask, request, render_template
import speech_recognition as sr
from pydub import AudioSegment
import subprocess
import random
import string
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

            # Get the current working directory
            current_dir = os.getcwd()

            # Loop through all files in the directory
            for file_name in os.listdir(current_dir):
                if file_name.endswith('.wav'):
                    file_path = os.path.join(current_dir, file_name)
                    os.remove(file_path)
                    print(f'Removed: {file_name}')
            audio_file = request.files["audio_file"]
            random_string =  ''.join(random.choices(string.digits, k=10))

            temp_filename = random_string +".mp3"
            audio_file.save(temp_filename)

            result = subprocess.run(['ffmpeg', '-i', random_string +".mp3",random_string +".wav"])

            # Save the audio file temporarily


            # Convert the audio file to text
            convt_text = convert_speech_to_text(random_string +".wav")

            # Remove the temporary file after processing
            os.remove(temp_filename)
    
    return render_template("index.html", convt_text=convt_text)

if __name__ == "__main__":
    app.run(debug=True)
