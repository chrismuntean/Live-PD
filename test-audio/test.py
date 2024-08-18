import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Path to the audio file
audio_file = "test-audio-1.wav"

# Path to the output text file
output_text_file = "outputfile.txt"

# Convert .wav to text
with sr.AudioFile(audio_file) as source:
    # Adjust for ambient noise and record the audio
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.record(source)

try:
    # Recognize the speech in the audio file
    text = recognizer.recognize_google(audio)
    print("Recognized Text: ", text)

    # Save the recognized text to a .txt file
    with open(output_text_file, "w") as file:
        file.write(text)

    print(f"Transcription saved to {output_text_file}")

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")