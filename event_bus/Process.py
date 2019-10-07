from threading import Thread
from time import sleep

from event_bus.Lamport import Lamport
from .Event import Event
# from geeteventbus.subscriber import subscriber
# from geeteventbus.eventbus import eventbus
# from geeteventbus.event import event
from .EventBus import EventBus


class Process(Thread):
    def __init__(self, name):
        Thread.__init__(self)

        self.setName(name)
        self.lamport = Lamport()
        self.bus = EventBus.get_instance()
        self.bus.register(self, 'Bidule')
        if self.getName() == "P1":
            self.bus.register(self, 'Machin')

        self.alive = True
        self.start()

    def post(self, event):
        self.lamport.send()
        event.counter = self.lamport.counter
        self.bus.post(event)

    def process(self, event):
        self.lamport.receive(event.counter)
        if not isinstance(event, Event):
            print(self.getName() + ' Invalid object type is passed.')
            return
        topic = event.get_topic()
        data = event.get_data()
        print(self.getName() + ' Processes event from TOPIC: ' + topic + ' with DATA: ' + data +
              " counter: {}".format(self.lamport.counter))

    def run(self):
        loop = 0
        while self.alive:
            print(self.getName() + " Loop: " + str(loop))
            sleep(1)

            b1 = Event(topic='Bidule', data="ga")
            b2 = Event(topic='Machin', data="bu")

            # self.post(b1)
            print(self.getName() + " send: " + b1.get_data() + " counter: {}".format(self.lamport.counter))
            if self.getName() == "P2":
                self.bus.post(b2)
                print(self.getName() + " send: " + b2.get_data() + " counter: {}".format(self.lamport.counter))

            loop += 1
        print(self.getName() + " stopped")

    def stop(self):
        self.alive = False
        self.join()
