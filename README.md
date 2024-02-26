# Chassis 2024

Chassis 2024 is a general purpose Python framework for integrating software infrastructure.  The goal of Chassis 2024 is to make reusing and combining essential infrastructure components as straightforward as possible.


#### Installation

```
pip install chassis2024
```

### Documentation

[Chassis 2024 is documented on github.io.](https://lionkimbro.github.io/chassis2024/)


### Longer Explanation

The idea of chassis2024 to make it so that you quickly reuse infrastructure.

"Infrastructure" here means things like:
* writing a lock file for your program
* reading config files
* setting up a GUI system (like tkinter), and running a main loop
* populating and processing argparse
* reading a persistence file, and writing back to it when closing

I wanted to make it trivial to combine infrastructure like these, together.

The central challenge was making sure that infrastructure steps are followed in the correct order.


## An Example

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

