import asyncio
import websockets

source_code = []
counter = 0

def readCode(name):
    try:
        f = open(name, "r")
        line = f.readline()
        while line:
            source_code.append(line)
            line = f.readline()
        f.close()
        return True
    except IOError:
        print("Could not read file:", name)
        return False


async def hello():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:
        path = input("Enter a path to your code file: ")

        isSuccess = readCode(path)
        if isSuccess:
           greeting = "Hello!"
           await websocket.send(greeting)
           print(f"Sending message to server: {greeting}")
           recvInfo = await websocket.recv()
           print(f"Received message from server: {recvInfo}")
           print(f"Sending code to server")
           await websocket.send(source_code)

asyncio.get_event_loop().run_until_complete(hello())
