
# CHASSIS2024_SPEC is the module attribute that is defined in
# (chassis-package)/__init__.py to declare that this module is a
# chassis2024 package.  It always defines a dictionary.
CHASSIS2024_SPEC = "CHASSIS2024_SPEC"

# What follows are keys in the CHASSIS2024_SPEC dictionary:
# EXECUTES_GRAPH_NODES -- a list of string names of execution graph
#   nodes, all of which are to be handled by the chassis package's
#   perform_execution_graph_node("...") fn.
EXECUTES_GRAPH_NODES = "EXECUTES_GRAPH_NODES"

# MAJOR STAGES
CLEAR = "CLEAR"
RESET = "RESET"
CONNECT = "CONNECT"
ACTIVATE = "ACTIVATE"
COOLDOWN = "COOLDOWN"
DEACTIVATE = "DEACTIVATE"
DISCONNECT = "DISCONNECT"
SHUTDOWN = "SHUTDOWN"

