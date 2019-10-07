from threading import Thread
from time import sleep

from .Event import Event
# from geeteventbus.subscriber import subscriber
# from geeteventbus.eventbus import eventbus
# from geeteventbus.event import event
from .EventBus import EventBus


class Process(Thread):
    def __init__(self, name):
        Thread.__init__(self)

        self.setName(name)

        self.bus = EventBus.getInstance()
        self.bus.register(self, 'Bidule')
        if self.getName() == "P3":
            self.bus.register(self, 'Machin')

        self.alive = True
        self.start()

    def process(self, event):
        if not isinstance(event, Event):
            print(self.getName() + ' Invalid object type is passed.')
            return
        topic = event.getTopic()
        data = event.getData()
        print(self.getName() + ' Processes event from TOPIC: ' + topic + ' with DATA: ' + data)

    def run(self):
        loop = 0
        while self.alive:
            print(self.getName() + " Loop: " + str(loop))
            sleep(1)

            b1 = Event(topic='Bidule', data="ga")
            b2 = Event(topic='Machin', data="bu")
            print(self.getName() + " send: " + b1.getData())
            self.bus.post(b1)
            if self.getName() == "P2":
                self.bus.post(b2)
                print(self.getName() + " send: " + b2.getData())

            loop += 1
        print(self.getName() + " stopped")

    def stop(self):
        self.alive = False
        self.join()
