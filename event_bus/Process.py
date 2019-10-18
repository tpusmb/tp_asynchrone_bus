from threading import Thread
from time import sleep

from event_bus.Lamport import Lamport
from .Event import Event
from .EventBus import EventBus
from .BroadcastEvent import BroadcastEvent
from .DedicatedEvent import DedicatedEvent


class Process(Thread):

    def __init__(self, name, bus_size):
        """
        Constructor of the class.
        :param name: (String) Name of the process.
        :param bus_size: (Integer) Number of process in the bus.
        """
        Thread.__init__(self)

        self.setName(name)
        self.bus_size = bus_size
        self.lamport = Lamport()
        self.bus = EventBus.get_instance()
        DedicatedEvent.subscribe_to_dedicated_channel(self.bus, self)
        BroadcastEvent.subscribe_to_broadcast(self.bus, self)

        self.alive = True
        self.token = False
        self.is_critical_section = False
        self.synch_request_counter = 0
        self.start()

    def post(self, event):
        """
        Post a message into the bus and update the Lamport clock.
        :param event: (Event) Event that contains the topic and the message.
        """
        self.lamport.send()
        event.counter = self.lamport.counter
        self.bus.post(event)

    def send_message(self, message, topic):
        """
        Creates an event and post it.
        :param message: (String) Message to send.
        :param topic: (String) Topic of the message.
        """
        event = Event(topic=topic, data=message)
        self.post(event)
        print(self.getName() + " send DATA: {} | TOPIC: {} | counter: {}".format(event.get_data(),
                                                                                 event.get_topic(),
                                                                                 self.lamport.counter))

    def process(self, event):
        """
        Function to receive an event and handle his message.
        :param event: (Event) Event that contains the topic and the message.
        """
        self.lamport.receive(event.counter)
        if not isinstance(event, Event):
            print(self.getName() + ' Invalid object type is passed.')
            return

        topic = event.get_topic()
        data = event.get_data()
        print(self.getName() + " receive DATA: {}"
                               " | TOPIC: {}"
                               " | counter: {}".format(data, topic, self.lamport.counter))

        if data is "token":
            self.token = True

        if data is "synchronization":
            self.synch_request_counter += 1

    def run(self):
        """
        Main loop of the process.
        """
        loop = 0
        self.synchronize()
        while self.alive:
            sleep(1)
            if self.synch_request_counter is not 0:
                self.on_synchronize()
            elif not self.is_critical_section or (self.is_critical_section and self.token):
                print(self.getName() + " Loop: {}".format(loop))
                self.on_token()

                self.send_message("ga", 'broadcast')

                if self.getName() == "P1":
                    self.send_message("bu", 'P2')

                loop += 1

        print(self.getName() + " stopped")

    def launch_token(self):
        """
         Give the token to this process.
        """
        self.token = True

    def on_token(self):
        """
        Handle the token.
        """
        if self.token:
            if self.is_critical_section:
                self.release()
            else:
                self.send_token()

    def request(self):
        """
        Set this process critical section to True.
        """
        self.is_critical_section = True

    def release(self):
        """
        Quit the critical section and send the token to the next process
        """
        self.is_critical_section = False
        self.send_token()

    def send_token(self):
        """
        Send the token to the next process.
        """
        target = (int(self.getName()[1:]) % self.bus_size) + 1
        self.send_message("token", "P{}".format(target))
        self.token = False

    def synchronize(self):
        """
        Send a message to every process.
        """
        self.send_message("synchronization", 'broadcast')

    def on_synchronize(self):
        """
        Check responses from other process to reset the synch_request_counter.
        """
        if self.synch_request_counter == self.bus_size:
            self.synch_request_counter = 0

    def stop(self):
        """
        Stop the process.
        """
        self.alive = False
        self.join()

