
import sys

from .words import *
from .exceptions import *
from . import kahn


# constants
kMAJOR_STAGES = [CLEAR, RESET, CONNECT, ACTIVATE, COOLDOWN,
                 DEACTIVATE, DISCONNECT, SHUTDOWN]
kPERFORM_EXECUTION_GRAPH_NODE_FN = "perform_execution_graph_node"


# globals

execution_spec = {}  # user supplied execution specification
chassis2024_package_objs = []  # [module object, ...]
execution_node_handlers = {}  # {str:node name: module object w/ perform_execution_graph_node(node name)}
execution_graph_sequences = []  # [(str:node name (before), str:node name (after), ...]
execution_node_order_calculated = []  # list of strings (node names)


# main functionality

def run(execution_spec_):
    _init()
    _populate_major_stages()
    execution_spec.update(execution_spec_)
    _locate_chassis2024_packages()
    _kahn()
    _execute()


def _init():
    """Clear all globals."""
    execution_spec.clear()
    del chassis2024_package_objs[:]
    execution_node_handlers.clear()
    del execution_graph_sequences[:]
    del execution_node_order_calculated[:]


def _populate_major_stages():
    i = 0
    for i in range(len(kMAJOR_STAGES)-1):
        execution_graph_sequences.append((kMAJOR_STAGES[i],
                                          kMAJOR_STAGES[i+1]))


def _locate_chassis2024_packages():
    for module_name, module_object in sys.modules.items():
        D = getattr(module_object, CHASSIS2024_SPEC, None)
        if D is not None:
            # Remember this module in global memory.
            chassis2024_package_objs.append(module_object)

            # Now store the graph nodes that it handles.
            for execution_graph_node in D[EXECUTES_GRAPH_NODES]:
                if execution_graph_node in execution_node_handlers:
                    error_info = {PACKAGE: moduleobj,
                                  EXECUTION_GRAPH_NODE: execution_graph_node}
                    raise MultiplePackagesHandlingExecutionGraphNode(error_info)
                else:
                    execution_node_handlers[execution_graph_node] = moduleobj


def _kahn():
    result = kahn.topological_sort(execution_graph_sequences)
    if result == kahn.CYCLE_DETECTED:
        raise ExecutionGraphCycleDetected()
    else:
        execution_node_order_calculated[:] = result


def _execute():
    # str:execution_graph_node (the name of the execution graph node)
    for execution_graph_node in execution_node_order_calculated:
        pkg = execution_node_handlers.get(execution_graph_node)
        if pkg is not None:
            # It's mandatory that this function exists.
            # An AttributeError will be raised if it isn't found -- rightly so.
            fn = getattr(pkg, kPERFORM_EXECUTION_GRAPH_NODE_FN)  # pkg.perform_execution_graph_node("...")
            fn(execution_graph_node)

