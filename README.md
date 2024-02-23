# Chassis 2024

Automatically sequence infrastructure initialization and teardown.

#### Installation

```
pip install chassis2024
```

### Brief Explanation

*(This is just a teaser.  [Read the github.io pages for more details and a full tutorial.](https://lionkimbro.github.io/chassis2024/))*

The idea of chassis2024 to make it so that you quickly reuse infrastructure.

"Infrastructure" here means things like:
* writing a lock file for your program
* reading config files
* setting up a GUI system (like tkinter), and running a main loop
* populating and processing argparse
* reading a persistence file, and writing back to it when closing

I wanted to make it trivial to combine infrastructure like these, together.

The central challenge was making sure that infrastructure steps are followed in the correct order.


### An Example: Hello, world!

Here's a "Hello, world!" program:

```
import sys

import chassis2024
import chassis2024.basicrun


CHASSIS2024_SPEC = {
    "INTERFACES": {"RUN": sys.modules[__name__]}
}


# interface: RUN
def run():
    print("Hello, world!")


if __name__ == "__main__":
    chassis2024.run()
```

## Execution Nodes

Chassis 2024 infrastructure positions itself  within an execution graph.

By default, the execution graph is very basic:

* #1 **CLEAR** -- the program begins
* #2 **RESET** -- the program is initialized
* #3 **ARGPARSE** -- Command Line arguments are parsed
* #4 **CONNECT** -- files are loaded, resources are connected
* #5 **ACTIVATE** -- user interface systems are activated
* #6 **UP** -- the program is running, main loop operations commense

This built-in system is fixed, but there is no default implementation, and it is very flexible, because Chassis 2024 infrastructure can extend the graph via module declarations.

An example from the ```chassis2024.argparse``` package:

```
CHASSIS2024_SPEC = {
    EXECUTES_GRAPH_NODES: [CLEAR_ARGPARSE, RESET_ARGPARSE, ARGPARSE],
    EXECUTION_GRAPH_SEQUENCES: [(CLEAR, CLEAR_ARGPARSE, RESET, RESET_ARGPARSE, ARGPARSE)],
    INTERFACES: {ARGPARSE: sys.modules[__name__]}
}
```

## Interfaces

The infrastructure pieces glue to one another through "interfaces."  Any object or module can be at the end of an interface, but ***only one*** thing can implement a given interface.

Similarly, each execution node can activate ***only one*** function.

## More Complex Example

```

import sys

import chassis2024
import chassis2024.basicrun
import chassis2024.argparse
import chassis2024.basicjsonpersistence
from chassis2024.words import *
from chassis2024.argparse.words import *
from chassis2024.basicjsonpersistence.words import *


this_module = sys.modules[__name__]


CHASSIS2024_SPEC = {
    INTERFACES: {RUN: this_module,
                 ARGPARSE_CONFIGURE: this_module}
}

EXECUTION_SPEC = {
    BASICJSONPERSISTENCE: {
        SAVE_AT_EXIT: True,
        CREATE_FOLDER: False,
        FILEPATH: "./echo_persistence_data.json"
    }
}


# interface: ARGPARSE_CONFIGURE
def argparse_configure(parser):
    parser.add_argument("-e", "--echo",
                        help="input string to echo",
                        default=None)
    parser.add_argument("-r", "--repeat-last",
                        dest="repeat",
                        help="repeat the last used echo string",
                        action="store_true")
    chassis2024.basicjsonpersistence.argparse_configure(parser)

# interface: RUN
def run():
    argparser = chassis2024.interface(ARGPARSE, required=True)
    D = chassis2024.interface(PERSISTENCE_DATA, required=True).data()
    if argparser.args.echo is not None:
        print(argparser.args.echo)
        D["msg"] = argparser.args.echo  # saved automatically
    else:
        print(D.get("msg", "use -e to specify string to echo"))


if __name__ == "__main__":
    chassis2024.run()
```
