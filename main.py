import os
import subprocess
import time
import speech_recognition as sr
from pydub import AudioSegment

# Initialize recognizer
recognizer = sr.Recognizer()

# Path to the FIFO pipe
fifo_path = "audio_pipe"

# Ensure the FIFO exists
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

# Start the FFmpeg process to stream audio into the pipe
ffmpeg_command = [
    "ffmpeg", "-i", "https://broadcastify.cdnstream1.com/12145",
    "-f", "s16le", "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", fifo_path
]

ffmpeg_process = subprocess.Popen(ffmpeg_command)

def process_audio_chunk(audio_chunk):
    """Processes a single audio chunk with Google Speech Recognition."""
    # Convert raw audio to AudioSegment
    audio_segment = AudioSegment(
        data=audio_chunk,
        sample_width=2,  # 16-bit audio
        frame_rate=16000,
        channels=1
    )

    # Export the AudioSegment to a wav file-like object for speech recognition
    with audio_segment.export(format="wav") as audio_file:
        audio_data = sr.AudioFile(audio_file)
        with audio_data as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                print("Transcription: " + text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

try:
    with open(fifo_path, 'rb') as fifo:
        while True:
            # Read 15 seconds of audio data
            audio_chunk = fifo.read(16000 * 2 * 15)  # 15 seconds of audio at 16 kHz, 16-bit mono

            if not audio_chunk:
                break

            process_audio_chunk(audio_chunk)

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    ffmpeg_process.terminate()
    os.remove(fifo_path)