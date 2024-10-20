<div align="center">

  # Live PD | [Live Demo](https://example.com)
  ### A Telegram bot that uses OpenAI's Whisper AI to transcribe live Police, Fire, EMS, Aviation, and Rail radio broadcasts from Broadcastify streams, delivering real-time updates to subscribers.
  ![GitHub commit activity](https://img.shields.io/github/commit-activity/t/chrismuntean/live-pd)
  ![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4%EF%B8%8F-blue)
  ![GitHub Release Date](https://img.shields.io/github/release-date/chrismuntean/live-pd)

</div>

## How it works
Live PD uses a [Broadcastify](https://www.broadcastify.com) audio stream to transcribe the transmissions with [OpenAI's Whisper](https://openai.com/index/whisper/) transcription AI model in 15 second chunks. It then sends these transciptions using [Telegram's API](https://core.telegram.org/bots) to a bot for alerts to anyone who starts the bot.