"""
File to run the TP.

Usage:
    Launcher.py <nb_process> [--dice]

Options:
    -h --help           Show this screen.
    <nb_process>        Number of process.
    --dice              Run the dice game.
"""
from event_bus.EventBus import EventBus
from event_bus.ProcessManager import ProcessManager
from time import sleep
from docopt import docopt

NB_PROCESS = 0


def normal_run():
    process_manager.add_process(NB_PROCESS)
    sleep(3)


def dice_game_run():
    print("\n -> Dice (1 to 100)\n")
    process_manager.add_dice_process(NB_PROCESS)
    process_manager.wait_round(5)
    print("\n -> Please check out the winner.txt file!\n")


if __name__ == '__main__':
    arguments = docopt(__doc__)

    bus = EventBus.get_instance()
    process_manager = ProcessManager()
    NB_PROCESS = int(arguments["<nb_process>"])
    if arguments["--dice"]:
        dice_game_run()
    else:
        normal_run()

    process_manager.stop_process()
    bus.stop()


