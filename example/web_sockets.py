# Julian Bonnells

import asyncio
import websockets
import json
import random

async def telemetry_server(websocket):
    print("Client connected")

    try:
        while True:
            # Generate random telemetry data
            telemetry_data = {
                "altitude": round(random.uniform(100, 10000), 2),  # Altitude in meters
                "speed": round(random.uniform(0, 900), 2),  # Speed in km/h
                "heading": round(random.uniform(0, 360), 2)  # Heading in degrees
            }

            # Convert to JSON and send to the client
            await websocket.send(json.dumps(telemetry_data))
            print(f"Sent telemetry data: {telemetry_data}")

            # Wait before sending the next update
            await asyncio.sleep(1)  # Adjust update frequency if needed
    except websockets.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(telemetry_server, "localhost", 4000):
        print("WebSocket server started on ws://localhost:4000")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())