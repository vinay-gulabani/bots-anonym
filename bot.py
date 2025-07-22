# bot.py
import asyncio
import websockets
import json

RENDER_WS_BASE = "wss://anonymous-messaging-backend.onrender.com/api/ws/"

BOT1_ID = "bot-user-1"
BOT2_ID = "bot-user-2"

async def bot(user_id, nickname, should_send_messages):
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
                        print(f"[{nickname}] Matched")

                    # Only this bot sends messages
                    if matched and should_send_messages and data.get("type") in ["matched", "message_sent"]:
                        await asyncio.sleep(60)
                        await websocket.send(json.dumps({
                            "type": "send_message",
                            "message": f"hi from {nickname}"
                        }))
                        print(f"[{nickname}] Sent message")

        except Exception as e:
            print(f"[{nickname}] Disconnected: {e}")
            await asyncio.sleep(5)

async def main():
    await asyncio.gather(
        bot(BOT1_ID, "BotOne", True),   # ✅ This one sends messages
        bot(BOT2_ID, "BotTwo", False)   # ❌ This one does not send messages
    )


if __name__ == "__main__":
    asyncio.run(main())
