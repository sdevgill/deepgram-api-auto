# Deepgram API Auto Transcription

A simple and easy-to-use audio transcription app that uses Deepgram's API
to transcribe audio files and calculate the transcription cost, automatically. It makes use of their latest model, [Nova](https://blog.deepgram.com/nova-speech-to-text-whisper-api/).

This implementation uses their paragraphs features, which is not available with OpenAI's Whisper. Using paragraphs in transcriptions enhances readability by providing structure and organization..

## Requirements

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/)

## Features

- Supports MP3, WAV, M4A and many more audio formats.
- Automatically transcribes all valid audio files in the input folder.
- Calculates the cost of each transcription based on the audio duration ($0.0043 currently).
- Saves transcriptions and costs in separate text files in the output folder.

## Installation

1. Clone this repository and navigate to the project folder

```
git clone git@github.com:sdevgill/deepgram-api-auto.git
cd deepgram-api-auto
```

2. Run `poetry install` to install the dependencies

```
poetry install
```

3. Activate the virtual environment

```
poetry shell
```

## Usage

1. Create an `.env` file in the project folder from the `.env.example` file

```
cp .env.example .env
```

2. Add your Deepgram API key to the `.env` file

```
DEEPGRAM_API_KEY=your-api-key
```

3. Create an `input` folder in the project folder and add your audio files to it

4. Run the app

```
python app.py
```
