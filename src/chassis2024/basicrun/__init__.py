# Copyright 2024 Lion Kimbro
# SPDX-License-Identifier: BSD-3-Clause

"""basic runner -- calls interface RUN's run() method"""


import chassis2024
from chassis2024.words import *


CHASSIS2024_SPEC = {
    EXECUTES_GRAPH_NODES: [UP]
}


# entry

def perform_execution_graph_node(n):
    if n == UP:
        chassis2024.interface(RUN).run()


