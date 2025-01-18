import os
from flask import Flask, render_template, request, jsonify
import pyttsx3
import speech_recognition as sr
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

app = Flask(__name__)

# Default location coordinates for H.A.L. Bengaluru (latitude, longitude)
default_location = (12.9756, 77.6101)

def speak_text(text):
    engine = pyttsx3.init()
    try:
        engine.say(text)
        engine.runAndWait()
    finally:
        engine.stop()

geolocator = Nominatim(user_agent="blinds_dog_app")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_navigation', methods=['POST'])
def start_navigation():
    try:
        audio_message = "Please tell me where you want to go."
        print(f"Audio message: {audio_message}")
        speak_text(audio_message)

        # Listen for the user's input (destination)
        destination = listen_audio()

        if destination:
            print(f"Destination recognized: {destination}")
            try:
                # Get coordinates for the destination using OpenStreetMap
                location = geolocator.geocode(f"{destination}, Bengaluru, India")
                if location:
                    destination_coords = (location.latitude, location.longitude)
                    distance = geodesic(default_location, destination_coords).km
                    # Assuming average walking speed of 5 km/h
                    travel_time = (distance / 5) * 60
                    response_message = f"Your destination is {destination}. Estimated walking time is {travel_time:.0f} minutes."
                    print(f"Response message: {response_message}")
                    speak_text(response_message)
                    return jsonify({
                        "message": response_message,
                        "coordinates": destination_coords,
                        "address": location.address
                    })
                else:
                    error_message = "Could not find the location. Please try again."
                    print(f"Error message: {error_message}")
                    speak_text(error_message)
                    return jsonify({"error": error_message}), 400
            except GeocoderTimedOut:
                error_message = "Location service timed out. Please try again."
                print(f"Error message: {error_message}")
                speak_text(error_message)
                return jsonify({"error": error_message}), 500
        else:
            error_message = "Could not recognize the destination. Please try again."
            print(f"Error message: {error_message}")
            speak_text(error_message)
            return jsonify({"error": error_message}), 400
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


def listen_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for input...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            print("Recognizing speech...")
            text = recognizer.recognize_google(audio)
            print(f"Recognition result: {text}")
            return text
        except sr.UnknownValueError:
            print("Error: Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Error: Speech recognition failed: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(debug=True)
