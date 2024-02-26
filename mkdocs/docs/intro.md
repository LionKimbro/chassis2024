
「Chassis 2024」へようこそ!

Have you ever found yourself juggling various bits of software infrastructure, wishing there was an easier way to piece them together? That's exactly why I created Chassis 2024.

Think about the usual tasks you handle when writing a program -- loading configuration files, ensuring your app runs only one instance at a time with lock files, or setting up (and later tearing down) the GUI system. Or perhaps you're starting to accept TCP services. And maybe these functionalities can be configured from CLI arguments, so you've got to set up argument parsing, too. It's a lot, right? Chassis 2024 is here to make these tasks feel like a breeze.

My goal was simple: to make reusing and combining these essential components as straightforward as possible. The cool part? With Chassis 2024, you don't have to worry about the sequence in which all these tasks happen. Thanks to some clever use of Kahn's algorithm for topological sorting, Chassis 2024 figures out the right order for you, ensuring everything runs smoothly and just as it should.

So, if you're looking to streamline your development process and make handling infrastructure feel like a walk in the park – if you want to jump past the boring parts and get straight to 'the good part,' give Chassis 2024 a try. It's all about making your life easier, one automated step at a time.

よろしくお願いします。


### Q: "What can I do with Chassis 2024?"

I'm just getting started with this, so there's not much here yet, but as I program, I will be collecting more and more pieces of infrastructure.

Here are things that you can do, today, with Chassis 2024:

* With [argparse](infra_argparse.md), you can automatically create and configure an [argparse](https://docs.python.org/3/library/argparse.html) argument parser.
* With [basicjsonpersistence](infra_basicjsonpersistence.md), you can automatically open a JSON file, when your program begins, and then automatically save it when the program ends.


### Q: "How do I learn to use Chassis 2024?"

There are two primary ways of using Chassis 2024:  (1) Making use of infrastructure, and (2) creating new infrastructure.  Knowing about the first comes first.  You might never want to create new infrastructure.  But if you want to, then you can learn that after learning the first.

I've provided a set of tutorials here.  They are intended to be followed sequentially.

Tutorial Set 1: (Making Use of Infrastructure)

* [The Basics: "Hello, World!"](ex_10_helloworld.md)
* [Accessing Interfaces: Echo](ex_20_echo.md)
* [Configuring Execution: Echo w/ Persistence](ex_30_echo2.md)

Tutorial Set 2: (Creating Infrastructure)

* ...

I haven't all of them yet, but I intend to write reference documentation over the course of March and April 2024, as well.

* [Infrastructure Documentation](infra_index.md) -- documents infrastructure that ships with the ```chassis2024``` package
* [Execution Nodes](ref_executionnode.md) -- documents the system of execution nodes and the default execution graph

