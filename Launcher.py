from time import sleep
from event_bus.EventBus import EventBus
from event_bus.ProcessManager import ProcessManager

if __name__ == '__main__':

    bus = EventBus.get_instance()

    process_manager = ProcessManager()
    # process_manager.add_process(3)
    process_manager.add_dice_process(3)

    sleep(6)

    process_manager.stop_process()

    bus.stop()
