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
                # Keep track of when last message was sent (only for send_messages=True)
                last_sent = None

                while True:
                    message = await websocket.recv()
                    data = json.loads(message)

                    if data.get("type") == "matched":
                        matched = True
                        print(f"[{nickname}] Matched!")

                    # Only BotOne sends messages every 60s
                    if matched and send_messages:
                        now = asyncio.get_event_loop().time()
                        if not last_sent or (now - last_sent >= 60):
                            await websocket.send(json.dumps({
                                "type": "send_message",
                                "message": f"Hi from {nickname} 👋"
                            }))
                            print(f"[{nickname}] Sent message")
                            last_sent = now

        except Exception as e:
            print(f"[{nickname}] Disconnected: {e}")
            await asyncio.sleep(5)

async def main():
    await asyncio.gather(
        bot(BOT1_ID, "BotOne", send_messages=True),   # ✅ Will send messages every 60s
        bot(BOT2_ID, "BotTwo", send_messages=False)   # ❌ Won’t send messages
    )

if __name__ == "__main__":
    asyncio.run(main())
