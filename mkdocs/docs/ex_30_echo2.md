

### An Example: Echo (with Persistence)

This time, we're adding data persistence to the program.

Here, you can begin to see the power of the chassis2024 system, start to show up.

This example [builds atop the first echo.py example](README_echo.md), which itself [builds atop the helloworld.py example, ...](README_helloworld.md)  Read those first, before attempting this example.


``` py
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
    chassis2024.run(EXECUTION_SPEC)
```


### Noticing

What's new here?

* ```import chassis2024.basicjsonpersistence```  -- More infrastructure: the ```chassis2024.basicjsonpersistence``` infrastructure.
* ```EXECUTION_SPEC```  -- it's defined just after the EXECUTION_SPEC, and then passed as an argument to ```chassis2024.run```.
* ```chassis2024.basicjsonpersistence.argparse_configure(parser)```  -- a call within ```argparse_configure(parser)```.
* ```D = chassis2024.interface(PERSISTENCE_DATA, required=True).data()```  -- in the *```run()```* routine, persistence data is accessed via interface.



