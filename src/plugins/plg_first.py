import sys
import time


def main(argv):
    if argv:
        if len(argv) > 0:
            if argv[0] == 'raise':
                print('Plugin RAISE!')

    for i in range(0, 100):
        print('Hello # {} from: {}'.format(i, __file__))
        time.sleep(3)

    print("Plugin {} complete work".format(__file__))


if __name__ == '__main__':
    main(sys.argv[1:])