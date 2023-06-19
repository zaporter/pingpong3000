import asyncio
import os
import cv2
from dotenv import load_dotenv
import time
import numpy as np

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.arm import Arm
from viam.components.camera import Camera
from viam.media.video import RawImage


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
    left_return_value = await left.get_image(mime_type="image/png")
    if isinstance(left_return_value,RawImage):
        print("Rawimg returned")
        exit(1)
    limg = left_return_value.convert('RGB')
    open_cv_image = np.array(limg)
    # convert to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy() 
    print(f"left get_image return value: {left_return_value}")
    lower_red = np.array([100,100,200])
    upper_red = np.array([230,190,255])
    mask = cv2.inRange(open_cv_image, lower_red, upper_red)
    res = cv2.bitwise_and(open_cv_image, open_cv_image, mask=mask)
    res = cluster(res)
    cv2.imwrite("./out/test.png", res)

    await robot.close()

def cluster(im):
    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# Threshold (in case we do morphology) and invert
    _, thresh = cv2.threshold(grey, 200, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite('DEBUG-thresh.png', thresh)

# Prepare to do some K-means
# https://docs.opencv.org/4.x/d1/d5c/tutorial_py_kmeans_opencv.html
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
# Find x,y coordinates of all non-white pixels in original image
    Y, X = np.where(thresh==0)
    Z = np.column_stack((X,Y)).astype(np.float32)

    nClusters = 3
    ret,label,center=cv2.kmeans(Z,nClusters,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

# Mark and display cluster centres 
    for x,y in center:
        print(f'Cluster centre: [{int(x)},{int(y)}]')
        cv2.drawMarker(im, (int(x), int(y)), [0,0,255])
    return im


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
    os.makedirs( "./out", exist_ok=True)
    asyncio.run(main())

