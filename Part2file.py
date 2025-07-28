
Speech_to_text.py
import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for speech... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=10)
            print("Processing...")
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
            return None
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
            return None