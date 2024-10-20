import os
import subprocess
import whisper
import numpy as np
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import asyncio
import functools

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
STREAM_URL = os.getenv("STREAM_URL")
STREAM_TITLE = os.getenv("STREAM_TITLE")

# Load the Whisper model
model = whisper.load_model("medium.en")

# FIFO pipe path
fifo_path = "audio_pipe"

# List to store chat IDs of subscribers
subscribers = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send a welcome message and subscribe the user 
    chat_id = update.effective_chat.id
    if chat_id not in subscribers:
        subscribers.append(chat_id)
        await context.bot.send_message(chat_id=chat_id, text=f"You've subscribed to {STREAM_TITLE} updates!")

async def send_message_to_subscribers(text: str):
    # Send the transcribed message to all subscribers 
    for chat_id in subscribers:
        message = f"<b><u>{STREAM_TITLE}</u></b>\n\"{text}\""
        await application.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")

async def process_audio_chunks():
    # Process audio chunks in a loop 
    # Ensure FIFO is removed and recreated
    if os.path.exists(fifo_path):
        os.remove(fifo_path)
    os.mkfifo(fifo_path)

    # FFmpeg command to stream audio and skip the first 30 seconds
    ffmpeg_command = [
        "ffmpeg", "-y", "-re", "-ss", "30", "-i", STREAM_URL,
        "-f", "s16le", "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", fifo_path
    ]
    ffmpeg_process = subprocess.Popen(ffmpeg_command)

    try:
        with open(fifo_path, 'rb') as fifo:
            print("Reading from FIFO pipe...")
            while True:

                # Read 15 seconds of audio
                audio_chunk = fifo.read(16000 * 2 * 15)
                if not audio_chunk:
                    print("No audio chunk received. Breaking...")
                    break

                # Process audio chunk asynchronously
                await process_audio_chunk(audio_chunk)

    except Exception as e:
        print(f"Error in audio processing: {e}")
        
    finally:
        ffmpeg_process.terminate()
        os.remove(fifo_path)
        print("FFmpeg process terminated and FIFO pipe removed.")

async def process_audio_chunk(audio_chunk):
    # Process a 15-second audio chunk using Whisper 
    audio_array = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0

    # Run the blocking whisper.transcribe in an executor to avoid blocking the event loop
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, functools.partial(model.transcribe, audio_array, language="en", fp16=False))
    transcription = result['text'].strip()
    print(f"Transcription: {transcription}")
    if transcription:
        await send_message_to_subscribers(transcription)

async def post_init(application: Application):
    # Function to run after the application is initialized 
    application.create_task(process_audio_chunks())

def main():
    global application
    # Set up the Telegram bot
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # Command handler for /start
    application.add_handler(CommandHandler("start", start))

    # Run the bot (this will process updates and keep the event loop running)
    print("Bot started. Waiting for updates...")
    application.run_polling()

if __name__ == "__main__":
    main()