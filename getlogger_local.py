import mss
import time
from multiprocessing import Process
from pynput.mouse import Listener as mouseListener
from pynput.keyboard import Listener as keyboardListener
from pynput.keyboard import Key
import os
import logging
import logging.config
import datetime


logging.basicConfig(format='%(asctime)s,%(message)s', level=logging.INFO, filename='logging_'+str(datetime.datetime.now())+'.csv', filemode='w')


def screen(path):
    if not os.path.isdir(path + 'screen'):
        os.mkdir(path + 'screen')
    while True:
        with mss.mss() as sct:
            screen_name = str(time.time())
            file = path + '/screen/' + screen_name + '.png'
            sct.shot(output=file)
            logging.info("{},{},{},{}".format('SCREEN',file,None,None))



def on_press(key):
    logging.info("{},{},{},{}".format('KEY_PRESSED',str(key), None, None))
    print('{0} pressed'.format(key))


def on_release(key):
    logging.info("{},{},{},{}".format('KEY_RELEASED', key, None))
    print('{0} release'.format(key))
    if key == Key.esc:
        return False


def on_move(x, y):
    logging.info("{},{},{},{}".format('MOUSE_MOVEMENT', x, y, None))
    print("Mouse moved position ({},{})".format(x, y))


def on_click(x, y, button, pressed):
    print("Mouse Position : {}".format((x, y)))
    logging.info("{},{},{},{}".format('MOUSE_CLICK', x, y, button))
    print("Mouse clicked button:{}".format(button))


def on_scroll(x, y, dx, dy):
    # screen(path_)
    print("Mouse Scrolling {}".format((x, y)))
    print("Mouse scrolled with ({},{})".format(dx, dy))


if __name__ == "__main__":

    path_ = input("Enter the path")
    p1 = Process(target=screen, args=(path_,))
    m = mouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    k = keyboardListener(on_press=on_press, on_release=on_release)
    m.start()
    k.start()
    p1.start()
    m.join()
    k.join()
    p1.join()
