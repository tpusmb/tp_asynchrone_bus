# tp_asynchrone_bus

This program will launch multiple process at the same time that will communicate all together.

## Installation

For this project you will need a python3 version.

You will need the following package:
    
    sudo apt install python3
    sudo apt install virtualenv
    sudo apt install python3-pip
    sudo apt install python3-tk
    sudo apt install cmake
 
Prepare your virtualenv:

    virtualenv -p python3 venv
    . venv/bin/activate
    pip install -r requirements.txt   

If you want to exit your virtualenv:

    deactivate

## Launch the program

To launch the program, run this command:

    python Launcher.py <nb_process> [--dice]
    
- **nb_process**: Number of process

- **dice**: Add this param to run the dice game.

#### Example

    python Launcher.py 3 --dice
    
This line will run the dice game with 3 process.

