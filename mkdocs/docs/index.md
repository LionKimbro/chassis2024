

# Chassis 2024

#### Abstract

Chassis 2024 streamlines software development by integrating and sequencing a variety of reusable infrastructure components with ease. Utilizing Kahn's algorithm for dynamic topological sorting, it seamlessly adapts to new tasks and requirements. Key features include automated loading and unloading of components like configuration files, GUI systems, lock file checks for single-instance execution, and network connection management. This ensures all elements operate in the correct sequence, simplifying the orchestration of complex software infrastructures for developers.

#### Installation

```
pip install chassis2024
```

### Introduction

ようこそ! Please allow me to introduce my project, Chassis 2024!

Have you ever found yourself juggling various bits of software infrastructure, wishing there was an easier way to piece them together? That's exactly why I created Chassis 2024.

Think about the usual tasks you handle when writing a program -- loading configuration files, ensuring your app runs only one instance at a time with lock files, or setting up (and later tearing down) the GUI system. Or perhaps you're starting to accept TCP services. And maybe these functionalities can be configured from CLI arguments, so you've got to set up argument parsing, too. It's a lot, right? Chassis 2024 is here to make these tasks feel like a breeze.

My goal was simple: to make reusing and combining these essential components as straightforward as possible. The cool part? With Chassis 2024, you don't have to worry about the sequence in which all these tasks happen. Thanks to some clever use of Kahn's algorithm for topological sorting, Chassis 2024 figures out the right order for you, ensuring everything runs smoothly and just as it should.

So, if you're looking to streamline your development process and make handling infrastructure feel like a walk in the park – if you want to jump past the boring parts and get straight to 'the good part,' give Chassis 2024 a try. It's all about making your life easier, one automated step at a time."

よろしくお願いします。


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
