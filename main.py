import os
import subprocess
import whisper
import numpy as np
import io
import soundfile as sf

# Load Whisper model for speech to text
model = whisper.load_model("medium")

# Path to the FIFO pipe
fifo_path = "audio_pipe"

# Make the FIFO pipe if it doesn't exist
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

# Start FFmpeg process to stream audio into the pipe
# Find other radio stations at https://www.broadcastify.com/listen/ then use developer tools to find the stream URL
ffmpeg_command = [
    "ffmpeg", "-y", "-i", "https://broadcastify.cdnstream1.com/12145",
    "-f", "s16le", "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", fifo_path
]
ffmpeg_process = subprocess.Popen(ffmpeg_command)

def process_realtime_audio(audio_buffer):
    # Convert raw audio buffer to a NumPy array
    audio_array = np.frombuffer(audio_buffer, dtype=np.int16).astype(np.float32) / 32768.0

    # Use Whisper to transcribe the audio data in the chunks
    result = model.transcribe(audio_array, fp16=False)
    print(f"Transcription: {result['text']}")

try:
    with open(fifo_path, 'rb') as fifo:
        while True:
            # Read 1 second of audio data (~32 KB)
            audio_chunk = fifo.read(16000 * 2 * 15)  # 15 seconds at 16kHz, 16-bit mono

            if not audio_chunk:
                break

            process_realtime_audio(audio_chunk)

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    ffmpeg_process.terminate()
    os.remove(fifo_path)