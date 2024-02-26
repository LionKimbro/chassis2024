
# Infrastructure Documentation: basicjsonpersistence

"Basic JSON Persistence" reads from a JSON file when your program begins, and saves the data back out when the program ends.


| | |
| :----- | :------------------------------------------ |
| title: | Basic JSON Persistence |
| import: | ```import chassis2024.basicjsonpersistence``` |
| words import: | ```from chassis2024.basicjsonpersistence.words import *``` |
| creates execution nodes: | ```CLEAR_BASICJSONPERSISTENCE```, ```RESET_BASICJSONPERSISTENCE```, ```READ_BASICJSONPERSISTENCE```, ```READ_PERSISTENCE``` |
| implements execution nodes: | ```CLEAR_BASICJSONPERSISTENCE```, ```RESET_BASICJSONPERSISTENCE``` |
| calls interfaces: | (None) |
| implements interfaces: | ```PERSISTENCE_DATA``` |


## Configuration

### Configuration via EXECUTION_SPEC

``` py
...
import chassis2024.basicjsonpersistence
from chassis2024.basicjsonpersistence.words import *
...

EXECUTION_SPEC = {
    BASICJSONPERSISTENCE: {
        SAVE_AT_EXIT: True,
        CREATE_FOLDER: True,
        FILEPATH: "./data/echo_persistence_data.json"
    }
}
```

| key | logical type | semantic type | default | description |
| --- | ------------ | ------------- | ------- | ----------- |
| ```SAVE_AT_EXIT``` | bool | - | True | whether to save the JSON file automatically on termination, or not |
| ```CREATE_FOLDER``` | bool | - | False | whether to create folders in the filepath, if they did not already exist |
| ```FILEPATH``` | str | relative or absolute filepath | "./persistent_data.json" | path to the JSON persistence file |


### Integration of ARGPARSE with Basic JSON Persistence

The design philosophy behind my implementation ensures that the [argparse](infra_argparse.md) module does not get influenced automatically by external factors. This approach is intended to grant the program comprehensive control over how command-line options are presented and managed.

Nonetheless, in practical scenarios, it's foreseeable that users utilizing the basicjsonpersistence module might frequently require the functionality to specify a file path for JSON persistence. To cater to this need, the module includes a specialized support function:

``` py
argparse_configure(parser, shortcutkey="-f", longkey="--persistence-filepath")
```

This function is designed to seamlessly align with the ARGPARSE_CONFIGURE interface. It allows for straightforward integration; you can directly assign the ARGPARSE_CONFIGURE interface to reference the basicjsonpersistence module's function if this is the sole argument parsing extension you are utilizing.

In more complex applications, where you have multiple argument parsing requirements, it is advisable to implement your own version of the ARGPARSE_CONFIGURE interface. Within this custom implementation, you can then explicitly invoke ```chassis2024.basicjsonpersistence.argparse_configure(parser)``` to integrate the JSON file path configuration capability into your argument parsing logic.

This method offers a modular and flexible approach, enabling the incorporation of JSON persistence configuration into a broader argument parsing strategy, tailored to the specific needs of your application.


## Execution Nodes

``` mermaid
graph TD
  clr["CLEAR"];
  clr_me[["CLEAR_BASICJSONPERSISTENCE"]];
  reset["RESET"];
  reset_me[["RESET_BASICJSONPERSISTENCE"]];
  argparse["ARGPARSE"];
  read_me[["READ_BASICJSONPERSISTENCE"]];
  read_persistence[["READ_PERSISTENCE"]];
  activate["ACTIVATE"];
  clr --> reset --> argparse --> activate;
  clr --> clr_me --> reset --> reset_me --> argparse --> read_me --> read_persistence --> activate;
  style clr_me stroke:#fff,stroke-width:2px;
  style reset_me stroke:#fff,stroke-width:2px;
  style read_me stroke:#fff,stroke-width:2px;
```

| execution node | what is done |
| -------------- | ------------ |
| CLEAR_BASICJSONPERSISTENCE | nulls ```.parsers```, ```.args``` |
| RESET_BASICJSONPERSISTENCE | nulls ```.parsers```, ```.args``` (redundant) |
| READ_BASICJSONPERSISTENCE | reads the file |


## Interfaces

### PERSISTENCE_DATA

The PERSISTENCE_DATA interface is intended for accessing loaded data, and for manually issuing ```save()``` instructions before the program exits.

| function | what it does |
| -------- | ------------ |
| .data() | returns the dictionary (which you are invited to modify) of loaded persistence data |
| .save() | forces an immediate save of the persistence data |
| .save_at_exit(False) | turns off exit-time persistence data saving |
| .save_at_exit(True) | turns back on exit-time persistence data saving |
| .save_at_exit() | returns whether exit-time persistence data saving is active or not (default is [True]) |


## Example Use

``` py hl_lines="6 9 21-25 38 43"
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

_[Read the "Echo (with persistence)" tutorial for a detailed examination of this example.](ex_30_echo2.md)_

