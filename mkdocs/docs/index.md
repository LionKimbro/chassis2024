

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

Learn By Example (Tutorial Material):

* 🙆 ["Hello, world!"](ex_10_helloworld.md) -- see a "Hello, world!" example
    * concepts: infrastructure, the CHASSIS2024_SPEC, interfaces
    * infrastructure: ```basicrun```
* 🙆 ["(Echo!)"](ex_20_echo.md) -- an "Echo" service, that responds to the CLI
    * concepts: using interfaces, words
    * infrastructure: ```argparse```
* ⚠ 工事中 -- [Echo with persistence](ex_30_echo2.md) -- an "Echo" service that remembers prior invocations
    * concepts: execution specs
    * infrastructure: ```basicjsonpersistence```
* 🙅 [???](ex_50_writing.md) -- writing infrastructure: a pid file
    * concepts: the execution graph, execution nodes
    * infrastructure: (???)

Learn By Concepts (Reference Material):

* 🙅 -- [Infrastructure Packages](ref_chassis2024spec.md) -- infrastructure packages are marked with a special identifier, ```CHASSIS2024_SPEC```
* 🙅 -- [Execution Nodes, Execution Graph](ref_executionnode.md) -- the execution graph, the key ordering principle behind the system
* 🙅 -- [Interfaces](ref_interfaces.md) -- "interfaces," a way that infrastructure pieces can find one another
* 🙅 -- [Execution Spec](ref_executionspec.md) -- the optional execution spec, which can configure execution

Announcements:

* [r/madeinpython -- Infrastructure Loading System: Chassis](https://www.reddit.com/r/madeinpython/comments/1ae8h3c/infrastructure_loading_system_chassis/)
