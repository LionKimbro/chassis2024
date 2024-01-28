
from .words import *
from .exceptions import *
from . import chassis


execution_spec = {}  # will be reset in run(...) call


def run(execution_spec = {}):
    """Execute the program, providing a specific execution specification."""
    chassis.run(execution_spec)

def interface(interface_name, required=False):
    """Access the object registered for a given interface.
    
    If it doesn't exist, and it's not required, return None.
    
    If it doesn't exist, and it's required, raises InterfaceUndefined.
    """
    found = chassis.interfaces.get(interface_name)
    if required and not found:
        raise InterfaceUndefined(interface_name)
    return found


