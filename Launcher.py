from time import sleep
from event_bus import Process
from event_bus import EventBus

if __name__ == '__main__':

    bus = EventBus.get_instance()

    p1 = Process("P1")
    p2 = Process("P2")

    sleep(3)

    p1.stop()
    p2.stop()

    bus.stop()
