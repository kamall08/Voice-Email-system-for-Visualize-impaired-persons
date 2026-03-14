import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 1

    with sr.Microphone() as source:
        print("Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("Listening...")

        try:
            audio = recognizer.listen(
                source,
                timeout=5,            # wait max 5 sec for speech
                phrase_time_limit=7   # stop listening after 7 sec
            )

            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print("You said:", text)

            return text.lower()

        except sr.WaitTimeoutError:
            print("Listening timed out")
            return None

        except sr.UnknownValueError:
            print("Could not understand audio")
            return None

        except sr.RequestError:
            print("Speech service unavailable")
            return None