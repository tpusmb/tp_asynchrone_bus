from threading import Thread
from time import sleep

from event_bus.Lamport import Lamport
from .Event import Event
# from geeteventbus.subscriber import subscriber
# from geeteventbus.eventbus import eventbus
# from geeteventbus.event import event
from .EventBus import EventBus
from .BroadcastEvent import BroadcastEvent
from .DedicatedEvent import DedicatedEvent


class Process(Thread):
    def __init__(self, name):
        Thread.__init__(self)

        self.setName(name)
        self.lamport = Lamport()
        self.bus = EventBus.get_instance()
        DedicatedEvent.subscribe_to_dedicated_channel(self.bus, self)
        BroadcastEvent.subscribe_to_broadcast(self.bus, self)

        self.alive = True
        self.start()

    def post(self, event):
        self.lamport.send()
        event.counter = self.lamport.counter
        self.bus.post(event)

    def send_message(self, message, topic):
        event = Event(topic=topic, data=message)
        self.post(event)
        print(self.getName() + " send: " + event.get_data() + " counter: {}".format(self.lamport.counter))

    def process(self, event):
        self.lamport.receive(event.counter)
        if not isinstance(event, Event):
            print(self.getName() + ' Invalid object type is passed.')
            return

        topic = event.get_topic()
        data = event.get_data()
        print(self.getName() + ' Processes event from TOPIC: ' + topic + ' | with DATA: ' + data +
              " | counter: {}".format(self.lamport.counter))

    def run(self):
        loop = 0
        while self.alive:
            print(self.getName() + " Loop: " + str(loop))
            sleep(1)
            self.send_message("ga", 'broadcast')

            if self.getName() == "P1":
                self.send_message("bu", 'P2')

            loop += 1
        print(self.getName() + " stopped")

    def stop(self):
        self.alive = False
        self.join()
