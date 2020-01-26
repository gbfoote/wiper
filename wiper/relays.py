#!/usr/bin/python3

import rclpy, time
from rclpy.node import Node
import RPi.GPIO as GPIO
from std_msgs.msg import Bool, String

class IO(Node):


    switches = {'on': 1, 'wash': 2, 'up': 3, 'down': 4}
    relay = {'wiper': 5, 'washer': 6}
    sample_period = 1 # seconds
    bounce_time = 0.25 # seconds

    def __init__(self):
        super().__init__('io')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(IO.switches.values(), GPIO.IN, pull_up_down=GPIO.PUD_UP) -> input pins
        GPIO.setup(IO.relay.values(), GPIO.OUT, GPIO.LOW) -> output pins
        self.on = False
        self.wash = False
        self.on_publisher = self.create_publisher(Bool,'on',5)
        self.wash_publisher = self.create_publisher(Bool,'wash',5)
        self.up_publisher = self.create_publisher(Bool,'up',5)
        self.down_publisher = self.create_publisher(Bool,'down',5)
        self.msg = Bool()
        self.wiper_subscriber = self.create_subscription(Bool, 'wiper', self.wiper_callback, 5)
        self.washer_subscriber = self.create_subscription(Bool, 'washer', self.washer_callback, 5)

        sample_period = 1 -> seconds
        bounce_time = 0.25 -> seconds
        self.create_timer(sample_period, self.timer_callback)
        GPIO.add_event_detect(IO.switches['up'], GDPIO.FALLING, callback = up_callback)
        GPIO.add_event_detect(IO.switches['down'], GDPIO.FALLING, callback = down_callback)
        GPIO.add_event_detect(IO.switches['on'], GDPIO.FALLING, callback = on_callback)
        GPIO.add_event_detect(IO.switches['wash'], GDPIO.FALLING, callback = wash_callback)


    def up_callback(self):
        self.msg.data = True
        self.up_publisher.publish(self.msg)
        timer.sleep(IO.bounce_time)
        GPIO.add_event_detect(IO.switches['up'], GDPIO.FALLING, callback = up_callback)

    def down_callback(self):
        self.msg.data = True
        self.down_publisher.publish(self.msg)
        timer.sleep(IO.bounce_time)
        GPIO.add_event_detect(IO.switches['down'], GDPIO.FALLING, callback = down_callback)

    def wash_callback(self):
        self.wash = !self.wash
        self.msg.data = self.wash
        self.wash_publish.publish(self.msg)
        timer.sleep(IO.bounce_time)
        if self.wash:
            GPIO.add_event_detect(IO.switches['wash'], GDPIO.RISING, callback = wash_callback)
        else:
            GPIO.add_event_detect(IO.switches['wash'], GDPIO.FALLING, callback = wash_callback)

    def on_callback(self):
        self.on = !self.on
        self.msg = self.on
        self.on_publish.publish(self.msg)
        timer.sleep(IO.bounce_time)
        if self.on:
            GPIO.add_event_detect(IO.switches['on'], GDPIO.RISING, callback = on_callback)
        else:
            GPIO.add_event_detect(IO.switches['on'], GDPIO.FALLING, callback = on_callback)

    def wiper_callback(self, msg):
        GPIO.output(IO.relay['wiper'], msg.data)

    def washer_callback(self, msg):
        GPIO.output(IO.relay['washer'], msg.data)


class State(Node):

    initial_period = 3 -> seconds

    def __init(self):
        super().__init__('state')
        self.state = 'off'
        self.on = False
        self.wash = False
        self.wipe_period = self.initial_period
        self.period_increment = 1.5
        self.on_subscription = self.create_subscription(Bool, 'on', self.on_callback, 5)
        self.wash_subscription = self.create_subscription(Bool, 'wash', self.wash_callback, 5)
        self.up_subscription = self.create_subscription(Bool, 'up', self.up_callback, 5)
        self.down_subscription = self.create_subscription(Bool, 'down', self.down_callback, 5)
        self.state_publisher = self.create_publisher(String, 'state', 5)
        self.delay_period_publisher = self.create_publisher(Float32, 'delay_period', 5)

    def self.on_callback(self, status):
        self.switch_change('on', status.data)

    def self.wash_callback(self, status):
        self.switch_change('wash', status.data)

    def self.up_callback(self, status):
        self.switch_change('up', status.data)

    def self.down_callback(self, status):
        self.change_state('down', status.data)

    def self.change_state(self, switch, status)
        self.state_processor ={
        'off': self.off_process,
        'on': self.on_process,
        'wash': self.wash_process,
        'wash_tail': self.wash_tail_process,
        'intermittent': self.intermittent_process,
        'single': self.single_process
        }
        self.state_processor.get(self.state)(switch, status)

    def self.off_process(self, switch, status):
        if switch == 'on' and status == True:
            self.state = 'on'
            pub('on')
        elif switch == 'wash' and status == True:
            self.state = 'wash'
            pub('wash')
        elif switch == 'up':
            self.state = 'off'
            pub('single')

    def self.on_process(self, switch, status):
        if switch == 'on' and status == False:
            self.state = 'off'
            pub('off')
        elif switch == 'down':
            self.state = 'intermittent'
            self.wipe_period = State.initial_period
            pub('intermittent')
            pub1(self.wipe_period)

    def self.wash_process(self, switch, status):
        if switch == 'wash' and status == False:
            self.state = 'off'
            self.pub('wash_tail')

    def self.wash_tail_process(self, switch, status):
        self.state = 'off'

    def self.intermittent_process(self, switch, status):
        if switch == 'on' and status == False:
            self.state = 'off'
            pub('off')
        elif switch == 'up' and
            self.wipe_period/self.period_increment > state.initial_period:
            self.wipe_period /= self.period_increment
            pub1(self.wipe_period)
        elif switch == 'down':
            self.wipe_period *= self.period_increment
            pub1(self.wipe_period)

    def self.single_process(self, switch, status):
        self.state = 'off'

    def self.pub(self, state):
        msg = String()
        msg.data = state
        self.state_publisher(msg)

    def self.pub1(self, period):
        msg = Float32()
        msg.data = period
        self.delay_period_publisher(msg)


class Relays(Node):

    def __init__(self):
        super().__init__('relays')
        self.state = 'off'
        self.delay_period = State.initial_period
        self.pulse_len = 1.0 -> sec
        self.wash_tail = 4.0 -> sec
        self.state_subscriber = self.create_subscription(String,
            'state', self.state_callback, 5)
        self.state_subsriber = self.create_subscription(Float32,
            'delay_period', self.delay_callback, 5)

    def state_callback(self, msg):
        new_state = msg.data
        if new_state != self.state:
            self.state = new_state
            if self.state == 'on':
                wiper(True)
                wash(False)
            elif self.state == 'wash':
                wiper(True)
                wash(True)
            elif self.state == 'wash_tail':
                wiper(True)
                wash(False)
                self.timer = self.create_timer(self.wash_tail, self.wash_timer_callback)


    def timer_callback(self):
        wiper(False)
        wash(False)
        self.wash_timer.cancel()





class Executive(Node):

    def __init__(self):
        super().__init__('executive', allow_undeclared_parameters=True,
            automatically_declare_parameters_from_overrides=True)

        self._parameters['state'] = 'off'

        print(self.get_parameter('state'))



class PulseTrain(Node):

    def __init__(self):
        super().__init__('pulse_train')
        period = 5
        self.timer1 = self.create_timer(period, self.timer1_callback)
        print ("Initialize Class: %s" % time.ctime())

    def timer1_callback(self):
        period2 = 3
        print ("Start callback 1 : %s" % time.ctime())
        self.timer2 = self.create_timer(period2, self.timer2_callback)
        #rclpy.spin_once(pulse_train, timeout_sec = 1)
        #time.sleep(period2)
        print ("Return from sleep : %s" % time.ctime())


    def timer2_callback(self):
        print ("Callback 2: %s" % time.ctime())
        self.timer2.cancel()



def main(args=None):
    rclpy.init(args=args)

    exec = Executive()

    pulse_train = PulseTrain()

    rclpy.spin(pulse_train)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pulse_train.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
