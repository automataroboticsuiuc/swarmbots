#!./automata/bin/python
from serial import Serial
from time import sleep

CMD_SHIFT      = 6
HALT           = 0x00
LINEAR         = 0x01
ARC            = 0x02
ROTATE         = 0x03
FW             = 0x1
BW             = 0x0
CW             = 0x1
CCW            = 0x0
WHEELBASE      = 4
DIRECTION_MASK = 0x01
RADIUS_SHIFT   = 1
DATA_MASK = 0xf8
DATA_SHIFT = 2


import sys,tty,termios

class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get():
    inkey = _Getch()
    while(1):
        k=inkey()
        # if k != '':
        #     break
        if k=='\x1b[A':
            print("up")
            return 1
        elif k=='\x1b[B':
            print("down")
            return 2
        elif k=='\x1b[C':
            print("right")
            return 3
        elif k=='\x1b[D':
            print("left")
            return 4
        else:
            print("not an arrow key!")
            return -1
    return -1

class Robot(object):
    def __init__(self, port):
        self.port = port
    def arc(self, radius, cw, fw):
        cmd = (ARC << CMD_SHIFT) | ((radius & 0x3F) << RADIUS_SHIFT) | cw | fw << 1
        self.port.write(chr(cmd))

    def halt(self):
        cmd = (HALT << CMD_SHIFT)
        self.port.write(chr(cmd))

    def linear(self, fw, data):
        cmd = (LINEAR << CMD_SHIFT) | fw | ((data & DATA_MASK) >> DATA_SHIFT)
        self.port.write(chr(cmd))
        print(format(cmd, '02x'))
        print(format(((data & DATA_MASK) >> DATA_SHIFT), '02x'))

    def rotate(self, cw, data):
        cmd = (ROTATE << CMD_SHIFT) | cw | ((data & DATA_MASK) >> DATA_SHIFT)
        self.port.write(chr(cmd))


def main():
    try:
        port = Serial('/dev/ttyUSB1', 9600)

        # while(True):
        #     c = get()
        #     if c==-1:
        #         port.write(chr(0))
        #         return
        #     port.write(chr(c))

        r = Robot(port)
        
        # print("Arc cw fw")
        # r.arc(10, 1, 1)
        # sleep(3)
        # print("Arc ccw fw")
        # r.arc(10, 0, 1)
        # sleep(3)
        # print("Arc cw bw")
        # r.arc(10, 1, 0)
        # sleep(3)
        # print("Arc ccw bw")
        # r.arc(10, 0, 0)
        # sleep(3)

        print("2")
        sleep(1)
        print("1")
        sleep(1)

        # print("255")
        # r.linear(FW, 255)
        # sleep(3)
        # print("100")
        # r.linear(FW, 100)
        # sleep(3)
        # print("50")
        # r.linear(FW, 50)
        # sleep(3)
        # r.rotate(CW, 140)
        # sleep(3)
        for i in range(4):
            print("Linear fw")
            r.linear(FW, 255)
            sleep(0.3)
            r.linear(BW, 255)
            sleep(0.1)
            print("Rotate cw")
            r.rotate(CW, 255)
            sleep(0.5)
            r.rotate(CCW, 255)
            sleep(0.1)
            r.halt()
            sleep(1.0)
        r.halt()


        # print("Linear bw")
        # r.linear(0)
        # sleep(3)

        # print("Rotate cw")
        # r.rotate(1)
        # sleep(3)
        # print("Rotate ccw")
        # r.rotate(0)
        # sleep(3)

        # print("Halt")
        # r.halt()
        # sleep(3)
        
        port.close()
        print("Done")
    except KeyboardInterrupt:
        r.halt()
        port.close()
        return

if __name__=='__main__':
        main()
