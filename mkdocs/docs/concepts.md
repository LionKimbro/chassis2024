
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
* **Establishing Logging:** Components for setting up loggers, or other kinds of reporting features.
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


