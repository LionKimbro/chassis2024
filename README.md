

# Chassis 2024

Automatically sequence infrastructure initialization and teardown.

#### Installation

```
pip install chassis2024
```

### Brief Explanation

The idea is to make it so that you quickly reuse infrastructure components.

"Infrastructure" here means things like:
* writing a lock file for your program
* reading config files
* setting up a GUI system (like tkinter), and running a main loop
* populating and processing argparse
* reading a persistence file, and writing back to it when closing

I wanted to make it trivial to combine these infrastructure together.

The central challenge was making sure that everything runs in the right order.


### Learn More

Example Programs:
* 🙆 ["Hello, world!"](README_helloworld.md) -- see a hello world example (```basicrun``` infrastructure)
* 🙆 ["(Echo!)"](README_echo.md) -- see a slightly more complex example (```argparse``` infrastructure)
* ⚠ 工事中 -- [Echo with persistence](README_echo2.md) -- see a still more complex example (```basicjsonpersistence``` infrastructure)

Key Concepts:
* 🙅 -- [Infrastructure Packages](README_chassis2024spec.md) -- infrastructure packages are marked with a special identifier, ```CHASSIS2024_SPEC```
* 🙅 -- [Execution Nodes, Execution Graph](README_executionnode.md) -- the execution graph, the key ordering principle behind the system
* 🙅 -- [Interfaces](README_interfaces.md) -- "interfaces," a way that infrastructure pieces can find one another
* 🙅 -- [Execution Spec](README_executionspec.md) -- the optional execution spec, which can configure execution

Walk-throughs:
* 🙅 -- [Writing Your Own Infrastructure](README_writing.md) -- a tutorial on how to write your own infrastructure package

