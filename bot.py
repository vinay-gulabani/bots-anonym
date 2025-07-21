# bot.py
import asyncio
import websockets
import json

RENDER_WS_BASE = "wss://anonymous-messaging-backend.onrender.com/api/ws/"

BOT1_ID = "bot-user-1"
BOT2_ID = "bot-user-2"

async def bot(user_id, nickname, send_messages=False):
    uri = f"{RENDER_WS_BASE}{user_id}"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print(f"[{nickname}] Connected")

                await websocket.send(json.dumps({
                    "type": "find_match",
                    "nickname": nickname
                }))

                matched = False
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)

                    if data.get("type") == "matched":
                        matched = True
                        print(f"[{nickname}] Matched!")

                    if matched and send_messages:
                        await asyncio.sleep(60)  # Wait 60 seconds
                        await websocket.send(json.dumps({
                            "type": "send_message",
                            "message": f"Hi from {nickname} 👋"
                        }))
                        print(f"[{nickname}] Sent message")

        except Exception as e:
            print(f"[{nickname}] Disconnected: {e}")
            await asyncio.sleep(5)

async def main():
    await asyncio.gather(
        bot(BOT1_ID, "BotOne", send_messages=True),   # ✅ Only BotOne sends messages
        bot(BOT2_ID, "BotTwo", send_messages=False)   # ❌ BotTwo only listens
    )

if __name__ == "__main__":
    asyncio.run(main())
