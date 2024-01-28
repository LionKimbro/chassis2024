
# CHASSIS2024_SPEC is the module attribute that is defined in
# (chassis-package)/__init__.py to declare that this module is a
# chassis2024 package.  It always defines a dictionary.
CHASSIS2024_SPEC = "CHASSIS2024_SPEC"

# What follows are keys in the CHASSIS2024_SPEC dictionary:
# EXECUTES_GRAPH_NODES -- a list of string names of execution graph
#   nodes, all of which are to be handled by the chassis package's
#   perform_execution_graph_node("...") fn.
EXECUTES_GRAPH_NODES = "EXECUTES_GRAPH_NODES"
# EXECUTION_GRAPH_SEQUENCES -- a list of string names of execution
#   graph nodes that must all follow after one another (though not
#   necessarily immediately after one another)
EXECUTION_GRAPH_SEQUENCES = "EXECUTION_GRAPH_SEQUENCES"
# INTERFACES -- a sequence of string names of interfaces, linked to
#   objects (typically: Python modules) that implement specific
#   interfaces (a collection of attributes and methods.)
#   ex: ("A", "B", "C", "M", "S", "W", "Z")
INTERFACES = "INTERFACES"

# MAJOR STAGES
CLEAR = "CLEAR"
RESET = "RESET"
ARGPARSE = "ARGPARSE"
CONNECT = "CONNECT"
ACTIVATE = "ACTIVATE"
UP = "UP"

# Exception Data
# MultiplePackagesHandlingExecutionGraphNode
PACKAGE = "PACKAGE"
EXECUTION_GRAPH_NODE = "EXECUTION_GRAPH_NODE"
# MultipleDefinitionsOfInterface
PACKAGE = "PACKAGE"
INTERFACE = "INTERFACE"
IMPLEMENTATION = "IMPLEMENTATION"

