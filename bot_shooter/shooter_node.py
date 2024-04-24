def main():
    print('Hi from bot_shooter.')


if __name__ == '__main__':
    main()
import imp
import rclpy
from rclpy.node import Node
import serial
from sensor_msgs.msg import Joy
from threading import Lock
from time import sleep


class ShooterNode(Node):

    def __init__(self):
        super().__init__('shooter_node')
        self.subscription = self.create_subscription(
            Joy,
            '/joy',
            self.controller_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.serial_port = '/dev/ttyUSB1'
        self.baud_rate = 57600
        self.conn = serial.Serial(self.serial_port, self.baud_rate, timeout=1.0)

        self.mutex = Lock()

    def controller_callback(self, msg):
       c_pressed = msg.buttons[1]
       s_pressed = msg.buttons[3]
       if c_pressed:
           print("c was presseed")
        #    for i in range(255):
           self.send_command(f"o {int(255)} {int(255)}")
       elif s_pressed:
           print("s was pressed")
        #    for i in range(255):
           self.send_command(f"o {int(-150)} {int(-150)}")
       else:
           print("nothing was pressed")
        #    self.send_command(f"o {int(1)} {int(1)}")
        #    self.send_command(f"o {int(-1)} {int(-1)}")
    
    

    def send_command(self, cmd_string):
        
        self.mutex.acquire()
        try:
            cmd_string += "\r"
            self.conn.write(cmd_string.encode("utf-8"))

            ## Adapted from original
            c = ''
            value = ''
            while c != '\r':
                c = self.conn.read(1).decode("utf-8")
                if (c == ''):
                    print("Error: Serial timeout on command: " + cmd_string)
                    return ''
                value += c

            value = value.strip('\r')

        finally:
            self.mutex.release()


        


def main(args=None):
    rclpy.init(args=args)

    shooter_node = ShooterNode()

    rclpy.spin(shooter_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    shooter_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
