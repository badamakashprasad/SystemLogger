from multiprocessing import Process
from pynput.mouse import Listener as mouseListener
from pynput.keyboard import Listener as keyboardListener
import socket
from PIL import ImageGrab
import pickle


HOST = '127.0.0.1'
PORT = 54124


def send_data(data, conn):
    print(len(pickle.dumps(data)))
    conn.sendall(pickle.dumps(data))


def on_click(x, y, button, pressed):
    send_data((x, y, button), conn[0])


def on_move(x, y):
    send_data((x, y), conn[1])


def on_press(key):
    send_data((key, 'P'), conn[2])


def on_release(key):
    send_data((key, 'R'), conn[3])


def screen_frame(conn):
    while True:
        img = ImageGrab.grab()
        send_data(img, conn[4])


if __name__ == '__main__':
    sock = [socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) for i in range(5)]
    conn = []
    addr = []
    for s in sock:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        c, a = s.accept()
        conn.append(c)
        addr.append(a)
        PORT += 1
    print(len(pickle.dumps(ImageGrab.grab())))
    for a in addr:
        print(a)
    m = mouseListener(on_move=on_move, on_click=on_click)
    k = keyboardListener(on_press=on_press, on_release=on_release)
    sc = Process(target=screen_frame, args=(conn,))
    k.start()
    m.start()
    sc.start()
    m.join()
    k.join()
    sc.join()
