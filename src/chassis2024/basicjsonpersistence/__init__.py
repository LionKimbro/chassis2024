"""load and save to a JSON file containing a dictionary


STAGES:
------------------------------------------------------------------------

  <CLEAR>
  + *CLEAR_BASICJSONPERSISTENCE  -- Nulls data
  <RESET>
  + *RESET_BASICJSONPERSISTENCE  -- Nulls data
  <ARGPARSE>
  + *READ_BASICJSONPERSISTENCE  -- reads data from JSON file
    READ_PERSISTENCE
  <ACTIVATE>

  (key):  <BUILT-IN EXECUTION NODE>
          + CREATED EXECUTION NODE
          *IMPLEMENTED_EXECUTION_NODE
             (executed via this module's
              .perform_execution_graph_node(n) implementation)


INTERFACES IMPLEMENTED:
------------------------------------------------------------------------

  Interface "PERSISTENCE_DATA":

    .data()  -- returns the dictionary of loaded persistence data
    .save()  -- forces an immediate save of the persistence data
    .save_at_exit(False)  -- turns off exit-time persistence data saving
    .save_at_exit(True)  -- turns back on exit-time persistence data saving
    .save_at_exit()  -- returns whether exit-time persistence data saving is
                        active or not (default is [True]: yes, saving,
                        though this is configurable in the execution spec.)


INTERFACES CONSUMED:
------------------------------------------------------------------------

  Interface "ARGPARSE"

    .args.persistence_file_filepath  -- checked for a specification of the
                                        persistence file's filepath
                                        (overrides execution-spec specified
                                         value)


CONFIGURATION PROCEDURES:
------------------------------------------------------------------------

  Typically, it is configured by way of the execution spec.

  (example:)
  ----------------------------------------------------------------------
  ...
  import chassis2024.basicjsonpersistence
  ...
  from chassis2024.basicjsonpersistence.words import *
  ...

  EXECUTION_SPEC = {
      BASICJSONPERSISTENCE: {
          SAVE_AT_EXIT: True,
          CREATE_FOLDER: True,
          FILEPATH: "./data/echo_persistence_data.json"
      }
  }
  ----------------------------------------------------------------------

  In the example above, a data/ folder will be created from the
  program's initial working directory, (if it wasn't there, it'll be
  created because CREATE_FOLDER is True, which, incidentally, is its
  default value), and then the file will be stored there at the
  program's completion.

  Also, SAVE_AT_EXIT here is True, which is redundant, because the
  default behavior is to to just that.  Set to SAVE_AT_EXIT: False if
  you want to turn this behavior off.

  If you want the user to be able to specify the filepath to the file,
  and you are using the built-in chassis2024.argparse component, you
  can make the work like so:
  
  ----------------------------------------------------------------------
  ...
  import chassis2024.basicjsonpersistence
  import chassis2024.argparse
  ...
  from chassis2024.basicjsonpersistence.words import *
  from chassis2024.argparse.words import *
  ...
  
  CHASSIS2024_SPEC = {
      INTERFACES: {...,
                   ARGPARSE_CONFIGURE: sys.modules[__name__],
                   ...}
  }

  # interface: ARGPARSE_CONFIGURE
  def argparse_configure(parser):
      ...
      chassis2024.basicjsonpersistence.argparse_configure(parser,
                                                          "-x",
                                                          "--xxx")
  ----------------------------------------------------------------------

  ...which will make it so that the filepath named after "-x" and with
  "--xxx" as a long form argument key, will work to specify the
  filepath.

  If you want to carefully craft your argument parsing, just make sure
  that you set the arguments "dest" to "persistence_file_filepath".


USE PROCEDURES:
------------------------------------------------------------------------

  Access the data via the .data() method on the interface.

  (by way of example:)
  ----------------------------------------------------------------------
  D = chassis2024.interface(PERSISTENCE_DATA, required=True).data()
  ----------------------------------------------------------------------

  Any changes you make to the dictionary, will be automatically saved
  when the program exits.

  /!\\ WARNING: This system is NOT durable!  If the process dies for
      any reason, including power-outtage, while the process is in the
      middle of writing the JSON data, then the JSON data will be
      corrupted, and there is no back-up.

      In the future, I intend to write a more durable data storage
      component.  This is just the "basic" JSON persistence system.

  If you want to save the data in the middle of execution:

  ----------------------------------------------------------------------
  chassis2024.interface(PERSISTENCE_DATA, required=True).save()
  ----------------------------------------------------------------------

  Exit-time saving is on by default.  This can be overridden in the
  execution spec.  It can also be toggled manually:

  ----------------------------------------------------------------------
  chassis2024.interface(PERSISTENCE_DATA, required=True).save_at_exit(False)
  ----------------------------------------------------------------------

  (If save_as_exit() is called without arguments, it returns whether
   save-at-exit is on or off, via True or False.)

  Note that during RESET_BASICJSONPERSISTENCE, the program is
  automatically reset to match the execution spec, defaulting to True.
"""


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


# constants

kDEFAULT_PERSISTENCE_FILEPATH = "./persistent_data.json"

# do NOT create folders, by default (execution spec key: CREATE_FOLDER)
kDEFAULT_CREATE_FOLDER_POLICY = False

kDEFAULT_SAVE_AT_EXIT = True

kARGPARSE_PERSISTENCE_FILE_FILEPATH = "persistence_file_filepath"


# globals

_data = None  # the data (will be a dictionary) kept in RAM
_save_at_exit = None  # whether to save at exit, or not [bool]
_filepath = None  # filepath to the persistence file [pathlib.Path]
_initial_cwd = None  # initial CWD [pathlib.Path]


# convert a string path to a pathlib.Path

def _str_to_path(str_path):
    """Convert string path specification to a pathlib.Path.
    
    Two critical considerations are:
    * ~/ is expanded to the user's home directory, cross-platform.
    * Relative paths are resolved relative to the execution's original
      working directory (which was recorded during the
      CLEAR_BASICJSONPERSISTENCE execution node.)
    """
    p = pathlib.Path(str_path).expanduser()
    if not p.is_absolute():
        return _initial_cwd / p
    else:
        return p


# read execution_spec

def _execution_spec_section():
    """Return the execution spec's BASICJSONPERSISTENCE, or else None."""
    return chassis2024.execution_spec.get(BASICJSONPERSISTENCE, None)

def _execution_spec_create_folder():
    """Return the CREATE_FOLDER value from the execution spec, or else None"""
    return (_execution_spec_section() or {}).get(CREATE_FOLDER)

def _execution_spec_persistence_file_filepath():
    """Return execution spec's filepath as a pathlib.Path, or else None
    
    Note:
    - returns as a pathlib.Path object
    - expands user (~/)
    """
    filepath = (_execution_spec_section() or {}).get(FILEPATH)
    return _str_to_path(filepath) if filepath else None

def _execution_spec_save_at_exit():
    """Return execution spec's SAVE_AT_EXIT, or else None."""
    return (_execution_spec_section() or {}).get(SAVE_AT_EXIT)


# ARGPARSE module cooperation

def argparse_configure(parser, shortkey="-f", longkey="--persistence-filepath"):
    group = parser.add_argument_group("Persistent Data",
                                      "Configuring persistent data access")
    group.add_argument(shortkey, longkey,
                       dest=kARGPARSE_PERSISTENCE_FILE_FILEPATH,
                       metavar="file",
                       help="path to persistence file",
                       default=(_execution_spec_persistence_file_filepath() or
                                kDEFAULT_PERSISTENCE_FILEPATH))

def _commandline_persistence_file_filepath():
    """If ARGPARSE component is in use, read the persistence filepath.

    Returns None if:
    * ARGPARSE component is not in use
    * it is in use, but it isn't being used to collect a persistence_file
    """
    parser = chassis2024.interface(ARGPARSE)
    if parser is None:
        return None
    else:
        p = getattr(parser.args, kARGPARSE_PERSISTENCE_FILE_FILEPATH, None)
        return _str_to_path(p) if p else None


# creating parent folders for _filepath, if required

def _create_folder_policy():
    """First, check the execution spec.  If not specified, return default."""
    # note: cannot be specified at command line, presently
    #       (an aesthetic decision)
    # first, check the execution spec;
    policy = _execution_spec_create_folder()
    if policy is None:
        # if it's not defined there, go to default
        return kDEFAULT_CREATE_FOLDER_POLICY
    else:
        return policy  # True or False

def _create_folder():
    if not _filepath.parent.exists():
        _filepath.parent.mkdir(parents=True)


# entry

def perform_execution_graph_node(n):
    global _initial_cwd, _save_at_exit, _data, _filepath
    if n == CLEAR_BASICJSONPERSISTENCE:
        _data = None
        _save_at_exit = None
        _filepath = None
        _initial_cwd = pathlib.Path.cwd()
        
    elif n == RESET_BASICJSONPERSISTENCE:
        _data = None
        _filepath = None
        # Take SAVE_AT_EXIT from the execution spec is defined,
        # otherwise, use kDEFAULT_SAVE_AT_EXIT.
        val = _execution_spec_save_at_exit()
        _save_at_exit = kDEFAULT_SAVE_AT_EXIT if val is None else val

    elif n == READ_BASICJSONPERSISTENCE:
        # First, make sure that while closing down, that the data is saved.
        chassis2024.chassis.call_before_termination(_do_final_save)

        # Set default values.
        _data = {}
        _filepath = _str_to_path(kDEFAULT_PERSISTENCE_FILEPATH)
        
        # override from execution spec, if available.
        _filepath = _execution_spec_persistence_file_filepath() or _filepath

        # override from CLI args, if available
        _filepath = _commandline_persistence_file_filepath() or _filepath
        
        # Read it (if the file exists)
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
    if _create_folder_policy():
        _create_folder()
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

