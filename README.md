<div align="center">

  # Live PD
  ### A Telegram bot that uses OpenAI's Whisper AI to transcribe live Police, Fire, EMS, Aviation, and Rail radio broadcasts from Broadcastify streams, delivering real-time updates to subscribers.
  ![GitHub commit activity](https://img.shields.io/github/commit-activity/t/chrismuntean/live-pd)
  ![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4%EF%B8%8F-blue)
  ![GitHub Release Date](https://img.shields.io/github/release-date/chrismuntean/live-pd)

</div>

## Installation
Begin by cloning the repository to your local machine:
```bash
git clone https://github.com/chrismuntean/Live-PD.git
```

Install dependencies
```bash
pip install -r requirements.txt
```
**Note**: You may want to do this inside of a Python virtual environment

## Configure environment variables
The .env file for this repository is structured as:
```bash
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
STREAM_URL=https://broadcastify.cdnstream1.com/12145
STREAM_TITLE=Phoenix PD
```

### How to get your own Telegram bot
See Telegram's tutorial on how to get your bot setup on their website [here](https://core.telegram.org/bots/tutorial)

### How to get a Broadcastify stream URL
Find the stream you would like subscriber's to recieve updates for on Brodcastify's website [here](https://www.broadcastify.com/listen/). Then use developer tools to find the raw stream broadcast URL under the network tab.

## Run the bot
```bash
python main.py
```

## Bot Screenshots

## How it works
Live PD uses a [Broadcastify](https://www.broadcastify.com) audio stream to transcribe the transmissions with [OpenAI's Whisper](https://openai.com/index/whisper/) transcription AI model in 15 second chunks. It then sends these transciptions using [Telegram's API](https://core.telegram.org/bots) to a bot for alerts to anyone who subscribes.