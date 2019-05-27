from multiprocessing import Process
import log_util


def script1():
    while True:
        import aws_subscribe_raspberry_listener


def script2():
    while True:
        pass


if __name__ == '__main__':
    log_util.log_info(__name__, 'Running scripts...')
    proc1 = Process(target=script1)
    proc1.start()
    log_util.log_info(__name__, 'Reading script running...')

    proc2 = Process(target=script2)
    proc2.start()
    log_util.log_info(__name__, 'Status script running...')

    log_util.log_info(__name__, 'Scripts running')
