import asyncio
import websockets
import pythonsqlite


async def hello(websocket, path):
    pythonsqlite.initialize_db()
    message = await websocket.recv()
    print(f"Received message from client: {message}")
    greeting = f"Hello!"

    await websocket.send(greeting)
    print(f"Sending message to client: {greeting}")

    try :
        sourceCode = await websocket.recv()

    except:
        print("Error while receiving source file")
        return

    print(f"Received code from client:\n{sourceCode} ")

    # Kompilacja przesłanego kodu
    output = pythonsqlite.compile_source_code(sourceCode)

    if output:
        await websocket.send("Successful compilation.")
    else:
        await websocket.send("Compilation failed.")

    pythonsqlite.insert_output(output, sourceCode)
    allProjects = pythonsqlite.select_all_projects()
    raport = pythonsqlite.generate_comparison_raport(allProjects, sourceCode)
    print("PRINTING REPORT")
    print(raport)

    await websocket.send(raport)


def example():
    print("example")

start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
