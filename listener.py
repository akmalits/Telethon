import os
import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv
import requests
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get values from .env file
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE')
channel_username = int(os.getenv('CHANNEL_USERNAME'))  # Convert to integer
session_name = os.getenv('SESSION_NAME', 'default_session')  # Unique session name for each account

# Create the client and connect
client = TelegramClient(f'/app/data/{session_name}', int(api_id), api_hash)

async def sign_in():
    """Sign in to Telegram or check if already authorized."""
    if not await client.is_user_authorized():
        # Send the login code if not authorized
        await client.send_code_request(phone_number)
        print("A login code has been sent to your Telegram account.")
        code = input("Enter the login code you received: ")
        await client.sign_in(phone_number, code)
        print("Successfully signed in!")
    else:
        print("Already authorized. Proceeding...")

async def save_data(content, timestamp):
    """Save data to the specified endpoint."""
    url = "http://web:3002/data/"  # Use the service name "web" for Docker internal communication
    data = {
        "content": content,
        "timestamp": timestamp
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print("Data saved successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to save data: {e}")

async def listen_for_messages():
    """Listen for new messages in the specified channel."""
    try:
        entity = await client.get_entity(channel_username)
    except ValueError as e:
        print(f"Cannot find any entity corresponding to {channel_username}")
        print(e)
        return
    
    @client.on(events.NewMessage(chats=entity, pattern='^(https?|ftp):\/\/([^\s$.?#].[^\s]*)$'))
    async def handler(event):
        print(f"New message in channel: {event.message.text}")
        await save_data(event.message.text, event.message.date.isoformat())

async def main():
    """Main function to handle the event loop."""
    while True:
        try:
            # Ensure the user is authorized
            await sign_in()

            # Start listening for messages
            await listen_for_messages()

            # Keep the client running
            print("Listening for new messages...")
            await client.run_until_disconnected()
        except Exception as e:
            print(f"An error occurred: {e}. Reconnecting in 10 seconds...")
            await asyncio.sleep(10)  # Wait before reconnecting

if __name__ == '__main__':
    try:
        # Run the Telegram client
        with client:
            client.loop.run_until_complete(main())
    except Exception as e:
        print(f"Failed to start the listener: {e}")