# MIT License

# Copyright (c) 2024 Concept Bytes

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from openai import OpenAI
import time
from dotenv import load_dotenv
from pathlib import Path
from pygame import mixer  # Load the popular external library
import speech_recognition as sr
import re
import os

tts_enabled = True

load_dotenv()  # Load environment variables from .env file

# Initialize the client with environment variables
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
mixer.init()

# Retrieve the assistant using environment variable
assistant = client.beta.assistants.retrieve(os.getenv('ASSISTANT_ID'))

# Create and retrieve the thread using environment variable
plant_thread = os.getenv('CHAT_THREAD_ID')
thread = client.beta.threads.retrieve(plant_thread)

def ask_question(question):
    global thread
    global thread_message
    thread_message = client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=question,
        )
    
    # Create a run for the thread
    run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant.id,
    )

    # Wait for the run to complete
    while True:
        run_status = client.beta.threads.runs.retrieve(
          thread_id=thread.id,
          run_id=run.id
        )
        if run_status.status == 'completed':
            break
        elif run_status.status == 'failed':
            return "The run failed."
        time.sleep(1)  # Wait for 1 second before checking again

    # Retrieve messages after the run has succeeded
    messages = client.beta.threads.messages.list(
      thread_id=thread.id
    )
    return messages.data[0].content[0].text.value



def play_sound(file_path):
    mixer.music.load(file_path)
    mixer.music.play()
    
# Function to generate TTS for each sentence and play them
def TTS(text):
    speech_file_path = Path(f"speech.mp3")
    speech_file_path = generate_tts(text, speech_file_path)
    play_sound(speech_file_path)
    while mixer.music.get_busy():  # Wait for the mixer to finish
        time.sleep(1)

    return "done"
            

# Function to generate TTS and return the file path
def generate_tts(sentence, speech_file_path):
    
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=sentence,
    )
    
    response.stream_to_file(speech_file_path)
    return str(speech_file_path)

