# Execution Nodes

Chassis 2024 is a Python framework designed to simplify the reuse of infrastructure components.  At the heart of Chassis 2024 lies the concept of execution nodes arranged into an execution graph.  These elements are fundamental to understanding how Chassis 2024 orchestrates the flow of operations within its framework, ensuring that every component interacts seamlessly and effectively.

This document aims to explain the concepts of execution nodes and the execution graph. Whether you are integrating new infrastructure, developing modules, or simply seeking to understand the inner workings of Chassis 2024, this guide will serve as your roadmap to understanding the role of execution nodes and the execution graph in the system.

Here's what the document covers:

* **Execution Nodes as Stages in Software Lifecycle:** This section delves into what execution nodes are and their significance in Chassis 2024.

* **Conceptual Use of Execution Nodes:** Focuses on the practical applications of execution nodes. It explores their potential uses in a conceptual manner, without delving into the specific coding details.

* **Technical Use of Execution Nodes:** This part gets into the nitty-gritty, detailing how execution nodes and the execution graph are utilized in code.

* **Default Execution Graph:** An overview of the standard execution graph provided with Chassis 2024.

* **Teardown:** Although the execution graph primarily facilitates reaching a running state, this section discusses the process of teardown, highlighting how decommissioning is scheduled.


## Execution Nodes as Stages in Software Lifecycle

In Chassis 2024, the execution graph is a dynamic and extensible framework, essential for orchestrating the flow of your application. It's designed to be effortlessly augmented by infrastructure modules, allowing developers to specify execution constraints like 'run after the "clearing" node' and 'run before the "argument parsing" node'. This extensibility is key; it means the execution graph can adapt and grow as new functionalities are integrated, without burdening the developer with the complexity of managing dependencies. Each addition is seamlessly woven into the existing structure, provided it doesn't create a cycle, which Chassis 2024 automatically checks for.

### A Concrete Example: Integrating Infrastructure

Consider a scenario in Chassis 2024 where your program has two fundamental infrastructure requirements:

1. Parsing Command Line Arguments
2. Reading from a Persistence File

Suppose you want to enable specifying the persistence file's location via command line.  The necessary sequence of operations is:

1. Initialize an `argparse.ArgumentParser`.
2. Add a command line option to the parser for specifying the persistence file.
3. Process the command line arguments using the parser.
4. Access the persistence file.

In Chassis 2024, this workflow is organized within the execution graph:

1. The argument parsing infrastructure introduces a node "CLEAR_ARGPARSE," which initializes a new `argparse.ArgumentParser`.  This node is configured to execute after "RESET" but before "ARGPARSE".
2. The persistence file infrastructure adds a node, "READ_PERSISTENCE", responsible for accessing the persistence file.  This node is set to follow "ARGPARSE" and precede "ACTIVATE."

(Note: The default built-in nodes, titled CLEAR, RESET, ARGPARSE, CONNECT, ACTIVATE, and UP, are detailed later in this document.)

In this manner, Chassis 2024 faciliates the easy expansion of the execution graph with new nodes like "CLEAR_ARGPARSE" and "READ_CONFIG", enhancing functionality while maintaining a straightforward and manageable workflow.


## Conceptual Use of Exection Nodes

### Association of Execution Nodes with Packages

In Chassis 2024, each execution node is typically associated with a specific package. When the system reaches an execution node, if it's associated with a package, that package's perform_execution_graph_node function is invoked with the execution node's name. This function performs the actions defined for that stage of the application's lifecycle.

### Declaration of Execution Node Sequences by Packages

Packages in Chassis 2024 declare their own sequences of execution nodes. This declaration includes specifying which nodes they will respond to and perform actions for. This mechanism allows packages to integrate their specific functionalities into the broader application flow.

### Single Package Association per Execution Node

To maintain clarity and order within the system, each execution node can only be associated with one package. If multiple packages attempt to associate with the same execution node, Chassis 2024 raises a MultiplePackagesHandlingExecutionGraphNode exception. This rule ensures a clear and unambiguous order of operations.

### Execution Graph Assembly and Execution by Chassis 2024

Chassis 2024 automatically assembles the execution graph based on the data collected from all packages, including their execution nodes and sequences. It then performs a topological sort of the graph to determine the execution order, ensuring that all dependencies and prerequisites are met.


## Technical Use of Execution Nodes

### Definition of CHASSIS2024_SPEC by Packages

Infrastructure packages in Chassis 2024 define a variable CHASSIS2024_SPEC, which declare the packages participation within the Chassis 2024 system.  This declaration includes keys like EXECUTES_GRAPH_NODES and EXECUTION_GRAPH_SEQUENCES, determining the execution nodes the package responds to and the sequences it adds to the overall execution graph.

Consider the following example from the [basicjsonpersistence](infra_basicjsonpersistence.md) package definition:

``` py
CHASSIS2024_SPEC = {
    # Nodes this package will execute
    EXECUTES_GRAPH_NODES: [CLEAR_BASICJSONPERSISTENCE,
                           RESET_BASICJSONPERSISTENCE,
                           READ_BASICJSONPERSISTENCE],
    # Sequences of nodes in the execution graph
    EXECUTION_GRAPH_SEQUENCES: [(CLEAR,
                                 CLEAR_BASICJSONPERSISTENCE,  # Node triggered by CLEAR
                                 RESET,
                                 RESET_BASICJSONPERSISTENCE,  # Node triggered by RESET
                                 ARGPARSE,
                                 READ_BASICJSONPERSISTENCE,  # Node triggered by ARGPARSE
                                 READ_PERSISTENCE,  # Signal completion of persistence load
                                 ACTIVATE)],
    ...
}
```


The EXECUTES_GRAPH_NODES key associates the package with the specific nodes: CLEAR_BASICJSONPERSISTENCE, RESET_BASICJSONPERSISTENCE, and READ_BASICJSONPERSISTENCE.  This list defines the nodes that this package is responsible for within the execution graph.

In the EXECUTION_GRAPH_SEQUENCES sub-key, the specified sequence (`CLEAR`, `CLEAR_BASICJSONPERSISTENCE`, `RESET`, etc.) outlines the order in which nodes should be activated. This sequence ensures a structured flow of execution. The tuple within the list allows for the definition of multiple sequences, providing flexibility and accommodating complex execution flows.

In summary, defining CHASSIS2024_SPEC ensures that infrastructure components in Chassis 2024 execute their instructions at the correct times.


### Execution of Nodes by Packages

One might wonder, "How exactly is an execution node activated within Chassis 2024?" The answer lies in the well-defined interaction between execution nodes and the packages responsible for them.

#### Role of the perform_execution_graph_node Function

Each infrastructure package defines a critical function: ```perform_execution_graph_node(execution_graph_node)```. This function is the heart of the node execution process.

* **Function Responsibility:** This function is responsible for executing the actions assigned to a specific execution nodes. When an execution node is reached in the graph, Chassis 2024 calls this function from the associated package.

* **Node-Specific Logic:** Inside this function, there is logic to handle different nodes. This is typically implemented using conditional statements, which check the name of the execution node passed as an argument and execute the corresponding actions.

For instance, consider the following snippet from the [basicjsonpersistence](infra_basicjsonpersistence.md) package:

``` py
def perform_execution_graph_node(n):
    ...
    if n == CLEAR_BASICJSONPERSISTENCE:
        # Actions for clearing basic JSON persistence (x1 execution)
        ...
    
    elif n == RESET_BASICJSONPERSISTENCE:
        # Actions for resetting basic JSON persistence
        ...

    elif n == READ_BASICJSONPERSISTENCE:
        # Actions for reading basic JSON persistence
        ...
```

In this example, the function perform_execution_graph_node contains specific actions for each of the execution nodes like CLEAR_BASICJSONPERSISTENCE, RESET_BASICJSONPERSISTENCE, and READ_BASICJSONPERSISTENCE.

#### Package-Node Association

* **Tracking Responsibility:** Chassis 2024 maintains a mapping of which package responds to each execution node. This is crucial for orchestrating the execution flow.

* **Execution Mechanics:** When the execution graph reaches a particular node, Chassis 2024 looks up the package associated with that node. It then locates the ```perform_execution_graph_node``` function within that package and invokes it, passing the name of the execution node as an argument.

This systematic approach ensures that each execution node is handled by its respective package in a structured and orderly fashion, contributing to the streamlined operation of the overall system.


## Default Execution Graph

Chassis 2024 comes with a predefined execution graph, which forms the backbone of its operational structure. This graph comprises several key nodes: CLEAR, RESET, ARGPARSE, CONNECT, ACTIVATE, and UP. Each node serves a specific purpose in the lifecycle of an application, ensuring a structured and efficient process flow. Below is a detailed description of each default node in the execution graph:

``` mermaid
graph TD
  clr["CLEAR"];
  reset["RESET"];
  argparse["ARGPARSE"];
  connect["CONNECT"];
  activate["ACTIVATE"];
  up["UP"];
  clr --> reset --> argparse --> connect --> activate --> up;
```

### CLEAR

The CLEAR node is the initial stage of the execution graph. It's designed for one-time setup tasks that are essential at the beginning of an application's lifecycle. Activities in this node include initializing internal data structures and pre-generating values that will remain constant throughout the operation of the application, such as pre-calculated trigonometric tables. This setup ensures that subsequent nodes operate on a well-prepared and stable groundwork.

### RESET

Following CLEAR is the RESET node. While CLEAR is for one-time initializations, RESET focuses on setups that might need to be repeated, particularly in testing scenarios. This node allows for the reinitialization of variables and states that may need resetting multiple times during an application's testing lifecycle. RESET is crucial for ensuring the application can return to a known state, which is especially important for iterative development and testing processes.

### ARGPARSE

The ARGPARSE node is dedicated to processing command line arguments. In this stage, the application parses any input parameters it requires before proceeding further. This ensures that all necessary inputs are correctly interpreted and available for use by the application, enabling it to adapt its behavior based on user inputs or configuration directives provided at launch.

### CONNECT

At the CONNECT node, the application establishes connections to necessary external resources. This could involve a wide range of activities, such as loading configuration files, reading necessary data from files, or establishing network connections with external systems and services. The CONNECT node is critical for integrating the application with the outside world and for accessing resources that are essential for its operation.

### ACTIVATE

Once all the necessary resources are connected, the ACTIVATE node takes over. This node is responsible for setting up the internal state of the application, which may involve cross-referencing and integrating data from multiple sources. It's also the stage where user interfaces are typically initialized, including graphical user interfaces (GUIs) or other interaction elements. ACTIVATE essentially prepares the application to start its main functionality.

### UP

Finally, the UP node represents the application's active running state. Here, the core functionalities of the program are executed. This is where the application performs its intended tasks, whether it's processing data, responding to user inputs, or any other primary operations for which the application was designed. The UP node is where the application delivers its value to the user.


## Teardown

Teardown is a crucial phase in the lifecycle of an application using Chassis 2024. It handles the orderly and safe shutdown or cleanup of processes that have been initiated by various execution nodes. This phase becomes especially important in maintaining the integrity and consistency of the application, particularly in scenarios where an abrupt termination or an unexpected exception occurs.

### Mechanism of Teardown

During the execution of nodes, it's common for certain setup or initialization actions to require corresponding cleanup actions. To manage this, Chassis 2024 provides a mechanism where nodes can register teardown callbacks through the ```chassis.call_before_termination(callback)``` function.

### Callback Registration

* **Function Usage:** Execution nodes can call ```chassis.call_before_termination(callback)``` to register a callback function for teardown activities.
* **Callback Function:** The callback function provided should take no arguments, and its return value is ignored.

Here's an example snippet from the [basicjsonpersistence](infra_basicjsonpersistence.md) package:

``` py hl_lines="11 14"
def perform_execution_graph_node(n):
    ...
    if n == CLEAR_BASICJSONPERSISTENCE:
        ...
        
    elif n == RESET_BASICJSONPERSISTENCE:
        ...

    elif n == READ_BASICJSONPERSISTENCE:
        # Make sure that while closing down, that the data is saved.
        chassis2024.chassis.call_before_termination(_do_final_save)
        ...

def _do_final_save():
    ...
```

### Execution Order of Callbacks

* **Reverse Order Execution:** These callbacks are executed in the reverse order of their registration. This reverse order ensures that the teardown process mirrors the setup process, maintaining a logical and efficient order of operations.
* **Example Scenario:** If an execution node A registers a callback cb_A, and a subsequent node B registers cb_B, the teardown process will first call cb_B and then cb_A.

### Teardown During Unhandled Exceptions

* **Exception Handling:** In the event of an unhandled exception occurring during the execution of nodes, Chassis 2024 ensures that the teardown process is still reliably executed.
* **Callback Invocation:** All registered callbacks are invoked in reverse order, just as they would be in a normal termination scenario. This ensures that even in the face of unexpected interruptions, the application can perform necessary cleanup, reducing the risk of corrupted states or resources being left in an indeterminate state.

