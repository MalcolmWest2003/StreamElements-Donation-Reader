import asyncio
import socketio
import requests
from pydub import AudioSegment
from pydub.playback import play

import config  # Make sure to have your config file with SOCKET_URL and SE_JWT_TOKEN

class StreamElements:
    def __init__(self):
        self.connection = socketio.AsyncClient()
        self.setup_event_callbacks()

    def setup_event_callbacks(self):
        """Setup the connection event callbacks"""
        self.connection.on("connect", self.on_connect)
        self.connection.on("disconnect", self.on_disconnect)
        self.connection.on("authenticated", self.on_authenticated)
        self.connection.on("event:test", self.on_event_test)
        self.connection.on("event", self.on_event)

    async def connect(self):
        await self.connection.connect(config.SOCKET_URL, transports=['websocket'])

    async def on_connect(self):
        await self.connection.emit("authenticate", {"method":"jwt","token":config.SE_JWT_TOKEN})

    async def on_disconnect(self):
        await self.connect()

    def on_authenticated(self, data):
        pass

    async def on_event_test(self, data, *args):
        event_type = data['listener']
        if event_type == 'tip-latest':
            self.handle_tip_event(data['event']['message'])

    async def on_event(self, data):
        event_type = data['listener']
        if event_type == 'tip-latest':
            self.handle_tip_event(data['event']['message'])

    def handle_tip_event(self, message):
        self.play_audio(message)

    def play_audio(self, message):
        response = requests.post(
            'https://api.eleven-labs.com/v1/speak',
            json={"text": message, "voice": "Joanna"},
            headers={'Authorization': f'Bearer {config.ELEVENLABS_API_KEY}'}
        )
        audio_data = response.content
        audio = AudioSegment.from_file_using_temporary_files(io.BytesIO(audio_data))
        play(audio)

async def main():
    streamelements = StreamElements()
    await streamelements.connect()

    # Wait indefinitely for events
    while True:
        await asyncio.sleep(1)  # This just prevents the loop from blocking

if __name__ == "__main__":
    asyncio.run(main())
