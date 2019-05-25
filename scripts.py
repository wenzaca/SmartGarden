from multiprocessing import Process


def script1():
    while True:
        pass


def script2():
    while True:
        pass


if __name__ == '__main__':
    print('Running scripts...')
    proc1 = Process(target=script1)
    proc1.start()
    print('Reading script running...')

    proc2 = Process(target=script2)
    proc2.start()
    print('Status script running...')

    print('Scripts running')
