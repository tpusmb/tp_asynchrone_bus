#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import timeit
import logging.handlers
from time import sleep
from event_bus.Process import Process
from event_bus.DiceProcess import DiceProcess

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/ProcessManager.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


class ProcessManager:

    def __init__(self):
        self.process_list = []

    def add_process(self, number_of_process):
        for i in range(number_of_process):
            self.process_list.append(Process("P{}".format(i + 1), number_of_process))
        self.process_list[len(self.process_list) - 1].launch_token()

    def add_dice_process(self, number_of_process):
        for i in range(number_of_process):
            self.process_list.append(DiceProcess("P{}".format(i + 1), number_of_process))
        self.process_list[len(self.process_list) - 1].launch_token()

    def wait_round(self, round_limit):
        end = False
        while not end:
            sleep(0.2)
            for process in self.process_list:
                if process.get_round() > round_limit:
                    end = True

    def stop_process(self):
        for process in self.process_list:
            process.stop()
