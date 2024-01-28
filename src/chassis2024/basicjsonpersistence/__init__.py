
import sys
import json
import pathlib

import chassis2024
from chassis2024.words import *

from ..words import *
from .words import *


CHASSIS2024_SPEC = {
    EXECUTES_GRAPH_NODES: [CLEAR_BASICJSONPERSISTENCE,
                           RESET_BASICJSONPERSISTENCE,
                           READ_BASICJSONPERSISTENCE],
    EXECUTION_GRAPH_SEQUENCES: [(CLEAR,
                                 CLEAR_BASICJSONPERSISTENCE,  # *
                                 RESET,
                                 RESET_BASICJSONPERSISTENCE,  # *
                                 ARGPARSE,
                                 READ_BASICJSONPERSISTENCE,  # *
                                 READ_PERSISTENCE,
                                 ACTIVATE)],
    INTERFACES: {PERSISTENCE_DATA: sys.modules[__name__]}
}


# globals

_data = None
_save_at_exit = True
_filepath = None


# entry

def perform_execution_graph_node(n):
    global _data, _filepath
    if n == CLEAR_BASICJSONPERSISTENCE:
        _data = None
    elif n == RESET_BASICJSONPERSISTENCE:
        _data = {}
    elif n == READ_BASICJSONPERSISTENCE:
        # First, make sure that while closing down, that the data is saved.
        chassis2024.chassis.call_before_termination(_do_final_save)

        # Next, locate the file to read.
        D = chassis2024.execution_spec[BASICJSONPERSISTENCE]
        folder = pathlib.Path(D[FOLDERPATH]).expanduser()
        
        if not folder.exists():
            if D[CREATE_FOLDER]:
                folder.mkdir(parents=True)
            else:
                raise FileNotFoundError(f"Folder not found: {folder}")
        
        _filepath = folder / D[FILENAME]
        
        # Read it
        if _filepath.exists():
            _data.clear()
            _data.update(json.load(open(_filepath)))

def _do_final_save():
    if _save_at_exit:
        save()


# interface PERSISTENCE_DATA

def data():
    return _data

def save():
    json.dump(_data, open(_filepath, "w"))

def save_at_exit(set_to=None):
    global _save_at_exit
    if set_to is None:
        return _save_at_exit
    elif set_to == True:
        _save_at_exit = True
    elif set_to == False:
        _save_at_exit = False
    else:
        raise ValueError(set_to)

