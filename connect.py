import asyncio
import os
import cv2
from dotenv import load_dotenv
import time

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.arm import Arm
from viam.components.camera import Camera


async def connect():
    secret = os.getenv("ROBOT_LOCATION_SECRET")
    if secret is None:
        print("No robot location secret set")
        exit(1)
    creds = Credentials(
        type='robot-location-secret',
        payload=secret)
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('ur5-main.3ce7ycobby.viam.cloud', opts)

async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)
    

    # right
    right = Camera.from_robot(robot, "right")
    right_return_value = await right.get_image()
    print(f"right get_image return value: {right_return_value}")
    
    # left
    left = Camera.from_robot(robot, "left")
    left_return_value = await left.get_image()
    print(f"left get_image return value: {left_return_value}")

    await robot.close()

async def benchmark_camera_fps():
    robot = await connect()
    print('Resources:')
    print(robot.resource_names)
    i=0
    num_seconds = 10
    start_time = time.time()
    while time.time() < start_time + num_seconds:
        i+=1
        right = Camera.from_robot(robot, "right")
        right_return_value = await right.get_image()
        print(f"right get_image return value: {right_return_value}")
        left = Camera.from_robot(robot, "left")
        left_return_value = await left.get_image()
        print(f"left get_image return value: {left_return_value}")

    print(f"{i} photos taken in {num_seconds} seconds")
    await robot.close()

if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())

