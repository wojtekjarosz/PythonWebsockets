import asyncio
import websockets

from io import StringIO
import sys


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
        code = compile(sourceCode, "code.py", 'exec')
        # redirect stdout to variable
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        exec(code)  # Wykonanie kodu

        # restore stdout
        sys.stdout = old_stdout

        print(mystdout.getvalue())

    except:
        print("Nie udało sie skompilowac kodu.")
        return False

    return True


start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
