
# Infrastructure Documentation: argparse


"Argument Parser" instantiates an [argparse.ArgumentParser,](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser) and makes it available for argument parsing.

Other execution nodes can configure the argument parser, once it has been created, and before arguments are parsed.

| | |
| :----- | :------------------------------------------ |
| title: | Argument Parser |
| import: | ```import chassis2024.argparse``` |
| words import: | ```from chassis2024.argparse.words import *``` |
| creates execution nodes: | ```CLEAR_ARGPARSE```, ```RESET_ARGPARSE``` |
| implements execution nodes: | ```CLEAR_ARGPARSE```, ```RESET_ARGPARSE```, ```ARGPARSE``` |
| calls interfaces: | ```ARGPARSE_CONFIGURE``` |
| implements interfaces: | ```ARGPARSE``` |



## Execution Nodes

``` mermaid
graph TD
  clr["CLEAR"];
  clr_arg[["CLEAR_ARGPARSE"]];
  reset["RESET"];
  reset_arg[["RESET_ARGPARSE"]];
  argparse["ARGPARSE"];
  clr --> reset --> argparse;
  clr --> clr_arg --> reset --> reset_arg --> argparse;
  style clr_arg stroke:#fff,stroke-width:2px;
  style reset_arg stroke:#fff,stroke-width:2px;
  style argparse stroke:#fff,stroke-width:2px;
```

* CLEAR_ARGPARSE -- nulls ```.parsers```, ```.args```
* RESET_ARGPARSE -- sets ```.parser``` to argparse.ArgumentParser instance, and calls ```.argparse_configure(parser)``` on the ARGPARSE_CONFIGURE interface
* ARGPARSE -- ```parser.parse_args()`` is called, and the result stored in ```.args```.

If you want to configure the argument parser, there are two ways to do it --

1. Implement the ARGPARSE_CONFIGURE interface, which is called in the RESET_ARGPARSE execution node.
2. Configure the argument parser during an execution node between RESET_ARGPARSE and ARGPARSE.


## Interfaces

### ARGPARSE

To access the argument parser or parsed arguments, you can access the module via the ARGPARSE interface.

It implements two data items:

* ```.parser``` -- this is the ```argparse.ArgumentParser``` instance, once the RESET_ARGPARSE execution node is complete, and can be meaningfully configured up until the ARGPARSE execution node runs
* ```.args``` -- this is the arguments parsed out from the ```argparse.ArgumentParser```, once the ARGPARSE execution node is complete

### ARGPARSE_CONFIGURE

When the ```argparse.ArgumentParser``` is first instantiated, a call is immediately made to ```.argparse_configure(parser)``` on the ARGPARSE_CONFIGURE interface.


## Example Use

``` py
import sys

import chassis2024
import chassis2024.basicrun
import chassis2024.argparse
from chassis2024.words import *
from chassis2024.argparse.words import *


this_module = sys.modules[__name__]


CHASSIS2024_SPEC = {
    INTERFACES: {RUN: this_module,
                 ARGPARSE_CONFIGURE: this_module}
}


# interface: ARGPARSE_CONFIGURE
def argparse_configure(parser):
    parser.add_argument("-e", "--echo",
                        help="input string to echo",
                        default="use -e to specify string to echo")

# interface: RUN
def run():
    argparser = chassis2024.interface(ARGPARSE, required=True)
    print(argparser.args.echo)


if __name__ == "__main__":
    chassis2024.run()
```

_[Read the "Echo" tutorial for a detailed examination of this example.](ex_20_echo.md)_
