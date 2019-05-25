import asyncio
import websockets

async def hello(websocket, path):
    message = await websocket.recv()
    print(f"Received message from client: {message}")
    greeting = f"Hello!"

    await websocket.send(greeting)
    print(f"Sending message to client: {greeting}")

    sourceCode = await websocket.recv()
    print(f"Received code from client:\n{sourceCode} ")


start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()