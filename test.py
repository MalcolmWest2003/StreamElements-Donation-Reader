# Import necessary libraries
import asyncio
import winsound
from enum import Enum
import socketio

import config
from elevenlabs import *

class EventName(Enum):
    connect = "connect"
    disconnect = "disconnect"
    authenticated = "authenticated"
    event = "event"

class StreamElements:
    def __init__(self):
        self.connection = socketio.AsyncClient()
        self.setup_event_callbacks()

    def setup_event_callbacks(self):
        """Setup the connection event callbacks"""
        self.connection.on(EventName.connect.value, self.on_connect)
        self.connection.on(EventName.disconnect.value, self.on_disconnect)
        self.connection.on(EventName.authenticated.value, self.on_authenticated)
        self.connection.on("event:test", self.on_event_test)
        self.connection.on("event", self.on_event)
        self.connection.on("event:update", self.on_event_update)
        self.connection.on("event:reset", self.on_event_reset)

    async def connect(self):
        await self.connection.connect(config.SOCKET_URL, transports=['websocket'])

    async def on_connect(self):
        print("Connected to StreamElements")
        await self.connection.emit("authenticate", {"method":"jwt","token":config.SE_JWT_TOKEN})

    async def on_disconnect(self):
        print("Disconnected from StreamElements")
        await self.connect()

    def on_authenticated(self, data):
        print(f"Authenticated with StreamElements ({data['message']})")

    async def on_event_test(self, data, *args):
        print("Data:", data)
        print("Extra arguments:", args)

    async def on_event_update(self, data):
        print("Received update event: ", data)

    async def on_event_reset(self, data):
        print("Received reset event: ", data)

        async def on_event(self, data):
         print("Received event: ", data)
         event_type = data['listener']
         print(f"Event type: {event_type}")
         if event_type == 'subscriber-latest':
            self.handle_subscriber_event(data['event'])

def handle_subscriber_event(self, data):
    print("handle_subscriber_event called")
    print(data)

    """Handle subscriber event and play the subscriber message as audio"""
    username = data.get('name')
    amount = data.get('amount')
    message = data.get('message')

    print(f"Subscription received from {username} for {amount}: {message}")

    # Play the audio
    self.play_audio('audio.wav')



async def main():
    streamelements = StreamElements()
    await streamelements.connect()

    # Wait indefinitely for events
    while True:
        await asyncio.sleep(1)  # This just prevents the loop from blocking

if __name__ == "__main__":
    asyncio.run(main())
