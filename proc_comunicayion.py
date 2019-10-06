import threading
from threading import Thread
import time
import os

check = threading.Condition()
globbiila = 'coma'


def func1():
    global globbiila
    print("funn1 started")
    globbiila = 'hhhahhahah'
    check.acquire()
    check.wait()
    print("got permission")
    print("funn1 finished")


def func2():
    global globbiila
    print("func2 started")
    check.acquire()
    time.sleep(2)
    check.notify()
    check.release()
    time.sleep(2)
    print("func2 finished")
    print(globbiila)


if __name__ == '__main__':
    Thread(target=func1).start()
    time.sleep(3)
    print("func2")
    check.acquire()
    check.notify()
    check.release()
    # Thread(target=func2).start()
