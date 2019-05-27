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

    # Kompilacja przesłanego kodu
    isSucces = compileSourceCode(sourceCode)

    if isSucces:
        # Jesli się udało to widomośc do klienta że sie udało
        await websocket.send("Successful compilation.")
    else:
        # Jeśli sie nie udalo to wiadomość że sie nie udało
        await websocket.send("Compilation failed.")


def compileSourceCode(sourceCode):
   try:
       code = compile(sourceCode,"code.py",'exec')
       #exec(code)      #Wykonanie kodu
       return True
   except:
       print("Nie udało sie spkompilowac kodu.")
       return False


start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()