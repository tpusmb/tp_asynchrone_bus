from threading import Thread
from time import sleep

from event_bus.Lamport import Lamport
from .Event import Event
from .EventBus import EventBus
from .BroadcastEvent import BroadcastEvent
from .DedicatedEvent import DedicatedEvent
from random import randint


class DiceProcess(Thread):
    def __init__(self, name, bus_size):
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
        self.dice = 0
        self.synch_request_counter = 0

        self.process_results = []

        self.start()

    def post(self, event):
        self.lamport.send()
        event.counter = self.lamport.counter
        self.bus.post(event)

    def send_message(self, message, topic):
        event = Event(topic=topic, data=message)
        self.post(event)
        print(self.getName() + " send: {} | counter: {}".format(event.get_data(), self.lamport.counter))

    def process(self, event):
        self.lamport.receive(event.counter)
        if not isinstance(event, Event):
            print(self.getName() + ' Invalid object type is passed.')
            return

        topic = event.get_topic()
        data = event.get_data()
        print(self.getName() + " Processes event from TOPIC: {}"
                               " | with DATA: {}"
                               " | counter: {}".format(topic, data, self.lamport.counter))

        if data is "token":
            self.token = True
        elif data is "synchronization":
            self.synch_request_counter += 1
        elif data is "run":
            self.dice_game()
        else:
            self.process_results.append(data)
            print(self.getName() + " process_result: {}".format(self.process_results))
            if len(self.process_results) == self.bus_size:
                self.check_winner()

    def run(self):
        sleep(1)
        self.dice_game()
        loop = 0
        while self.alive:
            print(self.getName() + " Loop: " + str(loop))
            sleep(1)
            self.on_token()

            loop += 1
        print(self.getName() + " stopped")

    def dice_game(self):
        self.process_results = []
        self.dice = randint(1, 6)
        self.synchronize()
        self.send_message(self.dice, 'broadcast')

    def launch_token(self):
        self.token = True

    def on_token(self):
        if self.token and not self.is_critical_section:
            self.release()

    def request(self):
        print(self.getName() + " request")
        while self.token is not True and self.alive is True:
            sleep(0.1)
        if self.token is True:
            self.is_critical_section = True
            self.write_winner()
            self.send_message("run", "broadcast")

    def release(self):
        target = (int(self.getName()[1:]) % self.bus_size) + 1
        self.send_message("token", "P{}".format(target))
        self.token = False

    def synchronize(self):
        self.send_message("synchronization", 'broadcast')
        while self.synch_request_counter < self.bus_size and self.alive is True:
            sleep(0.1)
        if self.synch_request_counter == self.bus_size:
            self.synch_request_counter = 0

    def stop(self):
        self.alive = False
        self.join()

    def check_winner(self):
        higer_result = 0
        for i in range(0, len(self.process_results)):
            print(self.getName() + " Comparison: {} & {}".format(higer_result, self.process_results[i]))
            if self.process_results[i] > higer_result:
                higer_result = self.process_results[i]
        if self.dice >= higer_result:
            self.request()

    def write_winner(self):
        file = open("winner.txt", "a+")
        file.write(self.getName() + "\n")
        file.close()

