import socket
import pickle
from multiprocessing import Process
import cv2
import numpy as np
import time

HOST = '127.0.0.1'
PORT = 54124
path = 'J:/python_projects/ScreenAutomate/screen'


def receive_data(buffer, length, conn):
    if buffer == -1:
        return pickle.loads(conn.recv(length))
    else:
        data = b''
        while len(data) < length:
            data += conn.recv(buffer)
        return pickle.loads(data)


def click(conn):
    while True:
        data = receive_data(-1, 4048, conn)
        print(data)
    # print("Mouse clicked on ({},{}) done by {}".format(data[0], data[1], data[3]))


def movement(conn):
    while True:
        data = receive_data(-1, 4048, conn)
        print(data)
    # print("Mouse movement ({},{})".format(data[0],data[1]))


def key_pressed(conn):
    while True:
        data = receive_data(-1, 4048, conn)
        print(data)


def key_released(conn):
    while True:
        data = receive_data(-1, 4048, conn)
        print(data)


def screen_frame(conn):
    while True:
        data = b''
        data = receive_data(-1, 3147326, conn)
        img = data
        img.save(path + '/' + str(time.time()) + '.png', 'PNG')

        # img_np = np.array(img)

        # frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        # frame.save('name.png')
        # imS = cv2.resize(frame, (960, 540))
        # cv2.imshow('screen', imS)
        # cv2.waitKey(1)


if __name__ == '__main__':
    sock = []
    for i in range(5):
        print(i)
        sock.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0))
        sock[i].connect((HOST, PORT))
        print(sock[i].getsockname())
        PORT += 1
    p_0 = Process(target=click, args=(sock[0],))
    p_1 = Process(target=movement, args=(sock[1],))
    p_2 = Process(target=key_pressed, args=(sock[2],))
    p_3 = Process(target=key_released, args=(sock[3],))
    p_4 = Process(target=screen_frame, args=(sock[4],))

    p_0.start()
    p_1.start()
    p_2.start()
    p_3.start()
    p_4.start()

    p_0.join()
    p_1.join()
    p_2.join()
    p_3.join()
    p_4.join()
