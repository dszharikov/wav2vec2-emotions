# Telegram Bot for Speech Emotion Recognition

This is a Telegram bot that can recognize emotions from speech using a pre-trained [Wav2Vec2](https://huggingface.co/Aniemore/wav2vec2-xlsr-53-russian-emotion-recognition) model based on the PyTorch framework. 

## Installation

1. Create a directory for the project.
2. Clone the repository: `git clone https://github.com/dszharikov/wav2vec2-emotions.git`
3. Create an environment: 

   For Venv:
   ```
   python -m venv env-name
   ```

   For Anaconda:
   ```
   conda create -n env-name
   ```
4. Install the requirements:

   ```
   pip install -r requirements.txt
   ```
   
   If you're using conda, you must first install `pip`: 
   
   ```
   conda install pip
   ```
   
5. Add your Telegram API token to the environmental variables or hard-code it into `bot_start.py`. 
6. Run `bot_start.py`.

   ```
   python bot_start.py
   ```

## Usage

Once you've added and started the bot, users can message the bot with their audio message. The bot will recognize the emotions from the speech.

## Acknowledgments

This project was built using the pre-trained [Wav2Vec2](https://huggingface.co/Aniemore/wav2vec2-xlsr-53-russian-emotion-recognition) model and the Python Telegram Bot wrapper, [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI). 
