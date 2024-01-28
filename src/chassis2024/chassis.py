
import sys
import traceback

import chassis2024

from .words import *
from .exceptions import *
from . import kahn


# constants
kMAJOR_STAGES = [CLEAR, RESET, ARGPARSE, CONNECT, ACTIVATE, UP]
kPERFORM_EXECUTION_GRAPH_NODE_FN = "perform_execution_graph_node"


# globals

chassis2024_package_objs = []  # [module object, ...]
execution_node_handlers = {}  # {str:node name: module object w/ perform_execution_graph_node(node name)}
execution_graph_sequences = []  # [(str:node name (before), str:node name (after), ...]
execution_node_order_calculated = []  # list of strings (node names)
interfaces = {}  # str:name to object that implements interface
call_before_termination_callbacks = []  # [fn() -> None, ...], last to first order
exception_type_value_tracebacks_encountered = []  # [(type, val, tb), ...]


# main functionality

def run(execution_spec):
    _init()
    _populate_major_stages()
    chassis2024.execution_spec.update(execution_spec)
    _locate_chassis2024_packages()
    _kahn()
    _execute()
    _call_before_termination_callbacks()
    _report_exceptions()

def call_before_termination(cb):
    call_before_termination_callbacks.append(cb)


def _init():
    """Clear all globals."""
    chassis2024.execution_spec.clear()
    del chassis2024_package_objs[:]
    execution_node_handlers.clear()
    del execution_graph_sequences[:]
    del execution_node_order_calculated[:]
    interfaces.clear()
    del call_before_termination_callbacks[:]
    del exception_type_value_tracebacks_encountered[:]


def _populate_major_stages():
    _define_execution_sequence(kMAJOR_STAGES)

def _define_execution_sequence(graph_sequence):
    i = 0
    for i in range(len(graph_sequence)-1):
        execution_graph_sequences.append((graph_sequence[i],
                                          graph_sequence[i+1]))


def _locate_chassis2024_packages():
    for module_name, module_object in sys.modules.items():
        D = getattr(module_object, CHASSIS2024_SPEC, None)
        if ((D is not None) and
            (D is not CHASSIS2024_SPEC)):  # ignore words.py
            # Remember this module in global memory.
            chassis2024_package_objs.append(module_object)

            # Now store the graph nodes that it handles.
            for execution_graph_node in D.get(EXECUTES_GRAPH_NODES, []):
                if execution_graph_node in execution_node_handlers:
                    error_info = {PACKAGE: moduleobj,
                                  EXECUTION_GRAPH_NODE: execution_graph_node}
                    raise MultiplePackagesHandlingExecutionGraphNode(error_info)
                else:
                    execution_node_handlers[execution_graph_node] = module_object

            # And note the graph edges that it requires.
            for graph_sequence in D.get(EXECUTION_GRAPH_SEQUENCES, []):
                _define_execution_sequence(graph_sequence)
            
            # Now store interfaces that it provides implementations for.
            for k, v in D.get(INTERFACES, {}).items():
                if k in interfaces:
                    error_info = {PACKAGE: moduleobj,
                                  INTERFACE: k,
                                  IMPLEMENTATION: v}
                    raise MultipleDefinitionsOfInterface(error_info)
                else:
                    interfaces[k] = v


def _kahn():
    result = kahn.topological_sort(execution_graph_sequences)
    if result == kahn.CYCLE_DETECTED:
        raise ExecutionGraphCycleDetected()
    else:
        execution_node_order_calculated[:] = result


def _execute():
    # str:execution_graph_node (the name of the execution graph node)
    try:
        for execution_graph_node in execution_node_order_calculated:
            pkg = execution_node_handlers.get(execution_graph_node)
            if pkg is not None:
                # It's mandatory that this function exists.
                # An AttributeError will be raised if it isn't found -- rightly so.
                fn = getattr(pkg, kPERFORM_EXECUTION_GRAPH_NODE_FN)  # pkg.perform_execution_graph_node("...")
                fn(execution_graph_node)
    # TODO: This should be configured through the system.
    #       When you import chassis2024.argparse,
    #       the CHASSIS2024_SPEC should include that
    #       SystemExit is permitted to pass through.
    #   Similarly, other modules could permit KeyboardInterrupt,
    #   and such, to pass through.
    except SystemExit:
        raise
    except:  # Yes, I really want to capture EVERYTHING else.
        _record_exception_details()


def _record_exception_details():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    exception_type_value_tracebacks_encountered.append((exc_type,
                                                        exc_value,
                                                        exc_traceback))

def _call_before_termination_callbacks():
    for cb in reversed(call_before_termination_callbacks):
        try:
            cb()
        except:  # Yes, I really want to capture EVERYTHING.
            _record_exception_details()
            # note that this DOES continue down the chain of callbacks


def _report_exceptions():
    # Check if there are any exceptions to report
    if not exception_type_value_tracebacks_encountered:
        # No exceptions to report.
        return

    # Iterate through each recorded exception
    L = exception_type_value_tracebacks_encountered
    for i, (exc_type, exc_value, exc_traceback) in enumerate(L, start=1):
        print(f"Exception {i}:")
        print(f"Type: {exc_type.__name__ if exc_type else 'None'}")
        print(f"Value: {exc_value}")

        # Format and print the traceback
        formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
        print("Traceback:")
        print(formatted_traceback)
        print("-" * 40)  # Separator for readability

