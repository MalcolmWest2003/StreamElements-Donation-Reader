# Import necessary libraries
import io
import os
import openai
import config
from pydub import AudioSegment
from pydub.playback import play
from elevenlabs import *
from elevenlabs.api import User
from colorama import Fore, Back, Style

# Set API Keys
elevenlabs_api_key = config.ELEVENLABS_API_KEY
openai_api_key = config.OPENAI_API_KEY
os.environ['ELEVENLABS_API_KEY'] = elevenlabs_api_key

# Initialize API Clients
set_api_key(elevenlabs_api_key)
openai.api_key = openai_api_key

# Create a user
user = User.from_api()

voices = Voices.from_api()

# Find the desired voice
omid = None
for voice in voices:
    if voice.name == "OmidLive":
        omid = voice
        break

# Adjust the settings
if omid is not None:
    omid.settings.stability = 0.25
    omid.settings.similarity_boost = 1
else:
    print("OmidLive voice not found!")

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def get_completion(messages, model="gpt-3.5-turbo", temperature=0.7):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

def text_to_speech(text, voice_id):
    response = generate(
        text=text,
        voice=voice_id  # use the voice_id here
    )
    return response

def play_audio(audio_bytes):
    audio = AudioSegment.from_file_using_temporary_files(io.BytesIO(audio_bytes))
    audio_file = audio.export(format="wav")
    audio_bytes = audio_file.read()  # Read bytes from the file
    audio_file.close()  # Close the temporary file
    play(audio_bytes)

def main():
    prompt = open_file('repeat.txt')
    conversation = [{"role": "system", "content": prompt}]
    first_request = True

    while True:
        user_input = input("USER: ")
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        conversation.append({"role": "user", "content": user_input})
        print("\n")
        response = get_completion(conversation)
        conversation.append({"role": "system", "content": response})
        print(f"OmidLive: {response}\n")


        audio_bytes = text_to_speech(response, omid)  # generate audio bytes from the text response
        audio = AudioSegment.from_file_using_temporary_files(io.BytesIO(audio_bytes))
        play_audio(audio_bytes)  # play the audio


        # Inside main() function and within your while loop...

        if "save clip" in user_input.lower():
            if not os.path.exists('saved_clips'):
                os.makedirs('saved_clips')
            filename = input("Enter a filename for the clip: ")
            filepath = f"saved_clips/{filename}.wav"
            audio.export(filepath, format="wav")
            print(f"Clip saved as {filepath}")
        

        first_request = False

if __name__ == "__main__":
    main()

