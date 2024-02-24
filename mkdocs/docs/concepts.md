
# Chassis 2024: Introduction to Core Concepts and Terminology

## Welcome to Chassis 2024

**Simplifying Software Infrastructure Management**

Welcome to Chassis 2024, a tool I designed to transform the experience of software development by simplifying the reuse of infrastructure components. With Chassis 2024, the aim is to eliminate the repetitive and tedious aspects of writing boilerplate code, allowing you to focus on the more creative and unique parts of your projects. By facilitating the easy instantiation and configuration of reusable components, and ensuring their orderly execution, Chassis 2024 makes software development more efficient and enjoyable.

In this guide, I'll introduce you to the core concepts and unique terminology of Chassis 2024, providing you with the foundational knowledge to effectively utilize this tool in your projects.


## Who Should Read This Guide

**Tailored for the Experienced Developer**

This guide is intended for intermediate to advanced programmers who already have a solid foundation in software development and are looking to explore innovative approaches in infrastructure management. It's particularly suited for those familiar with Python, including an understanding of Python modules, packages, and the standard library.

Prerequisite Knowledge:

* Proficiency in programming, particularly in Python.
* Familiarity with software architecture concepts and the challenges of software infrastructure management.

This guide is not designed for absolute beginners in programming. The concepts and implementations discussed require a certain level of technical proficiency and an understanding of advanced programming paradigms.

As you delve into this guide, Chassis 2024 will provide insights into managing reusable software components efficiently.


## Key Terminology in Chassis 2024

Understanding the specific terminology of Chassis 2024 is crucial for grasping its unique approach to software infrastructure. Here are key terms explained in the context of Chassis 2024:

### Infrastructure

In Chassis 2024, "infrastructure" refers to modular, reusable components integral to your software's structure and execution flow. Examples of infrastructure components include:

* **Configuration Management:** Modules for reading and applying configurations from external files.
* **Command-Line Argument Processing:** A component for interpreting command-line arguments to configure the software.
* **Lock File Management:** A mechanism to check for lock files, preventing simultaneous multiple instances of the application.
* **Persistent Data Management:** A component focused on managing persistent data, including reading persistence files at application start-up and writing them during program termination.
* **Network Operations:** Components for establishing and managing network operations, like TCP servers or database connections.
* **User Interface Management:** A component for setting up and managing user interfaces, such as initializing a graphical framework.

Chassis 2024 simplifies the integration and configuration of infrastructure components, orchestrating them into a single, properly ordered execution.


#### "Infrastructure" vs "Component"

The term "component" is commonly used in software architecture, but Chassis 2024 uses "infrastructure" to avoid confusion with systems like CORBA, COM, DCOM, Active X, microservices, or Python-specific systems like [Pluggy](https://pluggy.readthedocs.io/) or the [Zope Component Architecture](https://zopecomponent.readthedocs.io/en/latest/narr.html). While sharing some features with these architectures, Chassis 2024's focus is distinct.

"Infrastructure" in Chassis 2024 highlights the tool's unique approach to combining software components. Chassis 2024 focuses on the orchestration of loading sequences and teardown processes, ensuring that tasks are executed in the correct order and manner. This emphasis on execution order and seamless integration of elements sets Chassis 2024 apart from other architectures, which often prioritize inter-component communication.


### Execution Nodes

In Chassis 2024, "execution nodes" refer to distinct stages or points within the software's execution process. These nodes represent specific states or activities in the lifecycle of an application, such as initialization, operation, and termination. Chassis 2024 allows infrastructure to define execution nodes, and to precisely control and manage the order in which the execution nodes are executed. This concept is crucial for ensuring that each element of the infrastructure performs its designated function at the appropriate time in the overall execution flow.


### Execution Graph

The "execution graph" in Chassis 2024 is a representation of the relationships and dependencies between different execution nodes. It maps out how these nodes are interconnected, forming a structured pathway that guides the execution order of the software components. The graph is predominantly shaped by the infrastructure components within the system, with some predeclared nodes provided by Chassis 2024. Kahn's algorithm is applied to this graph to dynamically determine the optimal sequence for executing different parts of the application, ensuring efficiency and preventing conflicts or dependency issues.


### Interface

In Chassis 2024, an "interface" is a conceptual contract that defines the expected functionalities and attributes of modules within the system. Identified by unique string names, interfaces serve as a simple yet powerful way for modules to communicate their capabilities and roles. This system allows each interface to be implemented by only one module, promoting clear and direct interactions between different parts of the software. This streamlined approach to interfaces reflects Chassis 2024's emphasis on simplicity, flexibility, and clear, unambiguous connections within the software's architecture.


## Core Concepts

### Architecture Overview

Chassis 2024 is designed with a modular architecture, focusing on clear definitions and interactions among various infrastructure components within a software system. Here's an overview of how this architecture is organized and functions:

* **Module Infrastructure Declaration:** Modules in Chassis 2024 declare their role as part of the system's infrastructure by defining a CHASSIS2024_SPEC variable. This variable is a key element, tagging the module as infrastructure and providing essential information to the Chassis 2024 system. It can specify a range of details such as a list of implemented interfaces, extensions to the execution graph, or execution nodes managed by the module.

* **Importing Infrastructure Modules:** Modules explicitly import the infrastructure components they require. Each of these imported modules has its CHASSIS2024_SPEC defined, allowing the Chassis 2024 system to recognize and integrate them as part of the overall infrastructure. When chassis2024.run() is executed, the system dynamically scans sys.modules to identify all modules that define CHASSIS2024_SPEC, incorporating them into the execution process.

* **Program Initialization:** The initiation of Chassis 2024 typically occurs in a central module, often the one that starts the program (like package.__main__.py or a standalone module). This module will include a conditional statement if __name__ == "__main__" followed by the chassis2024.run() call. It is crucial that all necessary infrastructure modules are imported before this point, ensuring they are recognized and activated by the system upon startup.

* **Execution Specification:** During the execution of chassis2024.run(), the user has the option to provide an "execution spec" as the first argument. This specification acts as a configuration guide for the execution process, offering a way for modules to access shared configuration data through the chassis2024.chassis module. This feature adds an extra layer of flexibility, allowing for customized control over the execution flow based on the provided specifications.

Don't worry if this all seems a bit complex at first glance. In the upcoming tutorials, we'll be walking through each of these concepts in detail, with friendly introductions and practical examples. The aim is to make sure you're comfortable and fully understand how to leverage Chassis 2024's capabilities in your projects.


### Design Philosophy

The design philosophy of Chassis 2024 is built around several key principles:

* **Rapid Prototyping:** Chassis 2024 is engineered to enable rapid prototyping.  It achieves this by making it easy to incorporate and configure infrastructure, and by taking care of all execution timing issues.

* **Correctness Without Sacrificing Developer Time:** Chassis 2024 is committed to ensuring correctness in software execution without sacrificing the developer's time. Infrastructure components are designed to handle intricate details, such as locking mechanisms and PID file checks, ensuring that essential yet often overlooked aspects of software infrastructure are managed correctly. This approach allows developers to focus on writing engaging, innovative code, free from the burden of repetitive tasks that require meticulous attention to detail.

* **Flexibility and Modularity:** Embracing a modular approach, Chassis 2024 provides the flexibility to combine different (and even novel) infrastructure components as needed. This modularity means that the system can be adapted to a variety of applications, ensuring that each project's unique requirements are met efficiently.

* **Developer-Centric Design:** The system is created with the developer's workflow as a priority, focusing on features that enhance productivity and creativity. Chassis 2024 aims to make the development process not just more efficient but also more enjoyable.

* **Convention Over Configuration:** While offering customization, Chassis 2024 leans towards convention over configuration, providing sensible defaults that cover common scenarios. This approach eases the learning curve and reduces setup time, allowing developers to dive into the creative aspects of programming more quickly.

* **Emphasis on Execution Order:** Chassis 2024 places a strong emphasis on the execution order of software components. This ensures seamless operation and interaction among different parts of the system, addressing common challenges in complex software infrastructures.

* **Community and Collaboration:** It is my hope that other developers will see promise in this approach, and that a supportive community will develop around the Chassis system.  Collaboration and user feedback are crucial to evolve Chassis 2024 to meet the dynamic needs of its users.

This philosophy guides every facet of Chassis 2024, from its features to its user experience, ensuring that it remains a powerful yet user-friendly tool for efficient and correct software infrastructure management.


### Execution Flow


## How to Use This Guide

### As a Primer

### As a Reference


## Next Steps

### Moving to Practice

### Further Reading




I'd prefer to jump straight into code (such as [the Hello, World! tutorial,](ex_10_helloworld.md)) but there are some foundational concepts that really need to be explained up front.

### Terminology

Welcome to the first steps in learning Chassis 2024! In this tutorial, we'll explore the basics of creating a foundational "Hello, World!" program using Chassis 2024. This journey will be your gateway to understanding how Chassis 2024 streamlines software development by seamlessly integrating various infrastructure components.

**What We'll Cover:**

* **Getting Started:** We'll begin by setting up a basic Chassis 2024 environment, ensuring you have everything you need to start coding.
* **Code Anatomy:** Dive deep into the structure of a Chassis 2024 program. We'll dissect our 'Hello, World!' example, examining each part's role and how they work together.
* **Key Concepts:** Understand the crucial elements of Chassis 2024, including CHASSIS2024_SPEC and interface implementations. This will build your foundation for more advanced topics in future tutorials.

Through thought experiments at the end, we'll explore different scenarios, enhancing your understanding of how Chassis 2024 handles various situations.

**By The End of This Tutorial:**

You'll have a comprehensive understanding of setting up a basic Chassis 2024 project and the importance of its components, laying a solid foundation for tackling more complex scenarios with Chassis 2024.


いくぜ!

### Understanding the Basics via Hello, World!

Here's a "Hello, world!" program.

Copy it into a file called ```helloworld.py```, and run it.

(If you don't have chassis2024 installed, run ```pip install chassis2024``` to install it, first.)

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


### Things to Notice

So, what are we looking at here?

* **imports** -- There are two imports:
  * ```import chassis2024```
  * ```import chassis2024.basicrun```
* **```CHASSIS2024_SPEC```** -- a dictionary, with one key:
  * ```"INTERFACES"``` -- a declaration of an interface binding, specifically, ...
    * **```"RUN"```** -- the name of an interface, implemented by...
      * ```sys.modules[__name__]``` -- in Python, this means: "this module"

We'll talk about these piece by piece.

![visual breakdown of the code](https://github.com/LionKimbro/chassis2024/blob/main/img/helloworld_code_explanation.png?raw=true)

### import chassis2024

The first import is straightforward: ```import chassis2024```

That loads the chassis2024 system into memory (```sys.modules``` specifically).

### import chassis2024.basicrun

The second import is a little more mysterious: ```import chassis2024.basicrun```

What is ```chassis2024.basicrun```?  It's one of the built-in infrastructure package that ships with chassis2024.

Chassis 2024 programs are assembled from **infrastructure**.  Infrastructure basically means: a part of the system that has steps that must be followed, and that must be followed at particular times.

What ```chassis2024.basicrun``` does, is that *after everything else is set up,* it will call a *```run()```* function.

Q: "Which *run()* function will it run?"

A: We'll get to that.

Q: "How does it time things?"

A: We'll get to that -- much *later.*  It's a critical question, and central to what chassis2024 is, and how it works, but I can't answer that right now.  Just trust that there are ways to control timings.  But it's a good question to bear in mind.

The key things to understand right now, are that:

* ```import chassis2024``` -- This line imports the Chassis 2024 system as a whole, and...
* ```import chassis2024.basicrun``` -- ...this line includes the "basic run" infrastructure into our program's execution.

If you've got just that, you're good for the next piece.

### Understanding CHASSIS2024_SPEC

This identifier plays a pivotal role in Chassis 2024.  When you define ```CHASSIS2024_SPEC``` in your module, you're essentially tagging it as a piece of "infrastructure."  This tag is a univresal feature across all infrastructure components in Chassis 2024, signaling to the system that your module plays a crucial role in the overall architecture.

Here's how it works in the helloworld.py example:

``` py
CHASSIS2024_SPEC = {
    "INTERFACES": {"RUN": sys.modules[__name__]}
}
```

The Chassis 2024 system sees a definition of CHASSIS2024_SPEC, and recognizes, "This module is *infrastructure*."

*All* infrastructure packages and modules define ```CHASSIS2024_SPEC```.

Yes: ```chassis2024.basicrun``` has a ```CHASSIS2024_SPEC``` block at the top of it's implementation, because it is an infrastructure package, and all infrastructure packages define ```CHASSIS2024_SPEC```.

The Chassis 2024 system doesn't stop with recognizing "this is infrastructure," though -- it also *uses* the data that ```CHASSIS2024_SPEC``` is assigned to.

### "INTERFACES" and the "RUN" interface

Look again at the ```CHASSIS2024_SPEC``` definition:


``` py
CHASSIS2024_SPEC = {
    "INTERFACES": {"RUN": sys.modules[__name__]}
}
```

What does ```chassis2024``` make of ```"INTERFACES"```?  And what is the ```"RUN"``` interface all about?

This is a declaration to ```chassis2024``` binding "interfaces."  In particular, it's binding the ```"RUN"``` interface to the immediate module (```helloworld.py``` -- referring to itself via ```sys.modules[__name__]```).

**Interfaces are how infrastructure finds infrastructure.**  ```helloworld.py```, in writing this, is declaring that it is implementing the ```"RUN"``` interface.  Whenever someone asks ```chassis2024``` for the ```"RUN"``` interface implementor, it'll return the ```helloworld``` module back to the caller.

**Each interface can only be implemented by a single module.**  Interfaces have a "zero or one" relationship with the modules that implement them:  Either it's implemented, or it's not, and if it's implemented, it's implemented by only one single module.

If multiple modules attempt to implement the same interface, an exception is raised (```MultipleDefinitionsOfInterface```).

What an interface is good for is *not* rigorously defined by Chassis 2024.  There are no schemas, no interface classes and no interface definition objects,  there are no systems for discovery, or for publishing.  Rather, an interface is simply defined by a string identifier (like "RUN"), and by the expectations of use between the infrastructure that uses an interface, and infrastructure that meets an interface, held in the mind of the programmer(s).

When ```chassis2024.basicrun``` gets a hold of the thing at the other end of the ```"RUN"``` interface (```helloworld.py```, in this case,) it simply calls the *```run()```* function on it.  If it's not implemented, some sort of exception will be raised -- whatever exception is raised when you make a function call that isn't defined.  Your code will be in error.

```helloworld.py``` does not want to be in error, hence it implements the *```run()```* function:

``` py
# interface: RUN
def run():
    print("Hello, world!")
```

### Recap

OK, so -- you should be able to understand the program now:

``` py
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

![visual breakdown of the code's structure](https://github.com/LionKimbro/chassis2024/blob/main/img/helloworld_structure.png?raw=true)

* First, it imports the ```chassis2024``` system itself.
* Then, it imports the ```chassis2024.basicrun``` infrastructure.
* Then it declares itself to be infrastructure (by defining CHASSIS2024_SPEC).
  * In that declaration, it also declares that it implements the RUN interface.
  * Notably, it is the *sole implementer* of the RUN interface.  **All interfaces are only ever implemented once and there are no exceptions to this rule.**
* Then it defines the *```run()```* function, which by the way is the expectation of the "RUN" interface, by the ```chassis2024.basicrun``` infrastructure.
* And then, finally it runs ```chassis2024```.
  * The first thing chassis2024 will do, is examine all imported modules, and identify infrastructure.
    * It will find ```helloworld.py```.
      * It will note down that ```helloworld.py``` implements the ```"RUN"``` interface.
    * It will find ```chassis2024.basicrun```.
  * It will then assemble the execution graph.  [(You can skip ahead if you want to read more about the execution graph right away.)](ref_executionnode.md)
  * It will then execute all of the execution nodes.
  * When the system is up (in the "UP" execution node,) ```chassis2024.basicrun``` will call the ```"RUN"``` interface's *```run()```* method ...
  * ...which means that ```helloworld.run()``` is what will be called.

### Thought Experiments

#### Thought Experiment #1: Implementing RUN in a different module.

Q: "What if I imported another module, that had a CHASSIS2024_SPEC in it, and *that module* implemented the "RUN" interface instead?"

A: Then the ```MultipleDefinitionsOfInterface``` exception would be raised.

Q: "Oh, okay, -- but, -- what if I had taken out the CHASSIS2024_SPEC declaration from ```helloworld.py``` itself?"

A: That'd be okay then.  It'd call the ```run()``` function on the other module, then.

#### Thought Experiment #2: What if nobody implements RUN?

Q: "What if nobody implemented RUN?"

A: When it comes time to get the RUN interface, which is required by basicspec, then it'll raise an ```InterfaceUndefined``` exception.

Here's the relevant code from ```chassis2024/basicrun/__init__.py```:

``` py
def perform_execution_graph_node(n):
    if n == UP:
        chassis2024.interface(RUN, required=True).run()
```

...you can see it has "required=True" set, in it's call to resolve the interface, and then in ```chassis2024/__init__.py```,  ...

``` py
def interface(interface_name, required=False):
    """Access the object registered for a given interface.
    
    If it doesn't exist, and it's not required, return None.
    
    If it doesn't exist, and it's required, raises InterfaceUndefined.
    """
    found = chassis.interfaces.get(interface_name)
    if required and not found:
        raise InterfaceUndefined(interface_name)
    return found
```

See?  If ```required``` is ```true```, (and it is in the call from the ```basicrun``` source code,) if the interface name can't be found, it raises ```InterfaceUndefined("RUN")```, here.

### T-Junction

You arrive at a T-Junction.

You can [go left, to the Chassis 2024 title page.](index.md)

You can [go right, to the next example tutorial...](ex_20_echo.md)
