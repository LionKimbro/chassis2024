
# Infrastructure Documentation: basicrun


"Basic Run" is a simple one-shut execution runner.

After everything is setup, the program calls interface ```run()``` on interface "RUN".

| | |
| :----- | :------------------------------------------ |
| title: | Basic Run |
| module: | ```chassis2024.basicrun``` |
| creates execution nodes: | (None) |
| implements execution nodes: | ```UP``` |
| calls interfaces: | ```RUN``` |
| implements interfaces: | (None) |
| words import | (None) |


## Execution Nodes

When ```UP``` is reached (after all setup is complete,) ```basicrun``` calls function ```run()``` on the module that implements the ```RUN``` interface.

## Interfaces

### RUN

The RUN interface implements a single function: ```run()```, taking no parameters, and returning nothing.


## Example Use

``` py
# helloworld.py

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

_[Read the "Hello, world!" tutorial for a detailed examination of this example.](ex_10_helloworld.md)_