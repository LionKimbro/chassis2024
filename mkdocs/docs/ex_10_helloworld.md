
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

### CHASSIS2024_SPEC: Infrastructure Identifier

```CHASSIS2024_SPEC``` is a *special identifier*.  If it is defined in a module, it marks the module as **infrastructure**.

In our ```helloworld.py``` example, we have this declaration:

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
