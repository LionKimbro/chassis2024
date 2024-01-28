

### An Example: ECHO! Echo! echo! e..o!  e...!  ...!

Here's an "Echo" program.

We're building on top of knowledge from the last program, ```helloworld.py```.

[(I strongly urge you to read that one, before attempting this one.)](ERASEME_helloworld.md).

```echo.py```:

```
import sys

import chassis2024
import chassis2024.basicrun
import chassis2024.argparse
from chassis2024.words import *
from chassis2024.argparse.words import *


this_module = sys.modules[__name__]


CHASSIS2024_SPEC = {
    INTERFACES: {RUN: this_module,
                 ARGPARSE_CONFIGURE: this_module}
}


# interface: ARGPARSE_CONFIGURE
def argparse_configure(parser):
    parser.add_argument("-e", "--echo",
                        help="input string to echo",
                        default="use -e to specify string to echo")

# interface: RUN
def run():
    argparser = chassis2024.interface(ARGPARSE, required=True)
    print(argparser.args.echo)


if __name__ == "__main__":
    chassis2024.run()
```

### Noticing...

OK, things to notice:

* ```import chassis2024.argparse``` -- More infrastructure: the ```chassis2024.argparse``` infrastructure.
* ```from <...>.words import *``` -- "Words."  Lots of words.  We'll talk about it.
* interface ```"ARGPARSE_CONFIGURE"```
* interface ```"RUN"``` -- exactly as before
* ```argparser = chassis2024.interface(ARGPARSE, required=True)``` -- this is interface access, and we'll talk about it
* ```argparser.args.echo``` -- accessing the "echo" argument from the ArgumentParser.  Which we'll talk about.
* ```chassis2024.run()``` invocation -- just like last time (and working exactly the same) -- we will *not* talk about this again.

### "chassis2024.argparse" infrastructure

The most important piece here, is the incorporation of the ```chassis2024.argparse``` infrastructure.

What it does is -- after the modules have been cleared and reset [(which you can learn more about in the section on the execution graph, -- you might want to just take a peek at, real quick,)](README_executionnode.md) the argument parser is assembled, and then populated.  By "populated," I mean: arguments are defined on the argument parser.

It's populated by calling the ```ARGPARSE_CONFIGURE``` interface implementation (which: in this case, is defined to be in ```echo.py```):

```
CHASSIS2024_SPEC = {
    INTERFACES: {RUN: this_module,
                 ARGPARSE_CONFIGURE: this_module}
}
```

Now, the argument parser, we must be clear, is [the Python "batteries included" argparse.ArgumentParser.](https://docs.python.org/3/library/argparse.html)  Detailing it and how it works, is beyond the scope of this Chassis 2024 documentation.

If you understand argparse.ArgumentParser, though, then this will be clear:

```
# interface: ARGPARSE_CONFIGURE
def argparse_configure(parser):
    parser.add_argument("-e", "--echo",
                        help="input string to echo",
                        default="use -e to specify string to echo")
```

You might be wondering, though:  "How do you get at the arguments that were parsed out?"

That's the very next subject.

### Accessing the ARGPARSE Interface

It's in this code, here:

```
#interface: RUN
def run():
    argparser = chassis2024.interface(ARGPARSE, required=True)
    print(argparser.args.echo)
```

The first thing that the *```echo.run()```* function does, is load the ```"ARGPARSE"``` interface.

The ```chassis2024.argparse``` package implements it.  The implementation of "ARGPARSE" essentially means that it has two identifiers defined on it:  ```.parser```, and ```.args```.  After the parse happens [(and we'll talk about the execution nodes and timing,)](README_executionnode.md) then ```.args``` has the arguments loaded into it, by the time *```run()```* is called.

Since the ```RUN``` interface is called by ```chassis2024.basicrun``` as the last thing in the execution graph, it's guaranteed to be filled by this time.

#### ...a quick question about chassis2024.interface calls...
Q: "I see that it says, ```required=True```.  What if ```"ARGPARSE"``` had not been defined?"

A: Well, the interface is bound by the ```chassis2024.argparse``` package.  But let's say it hadn't been.  Then when that call to ```chassis2024.interface(ARGPARSE, required=True)``` is called, it'll raise ```InterfaceUndefined```.

Q: "And what if required was ```required=False```?"

A: If it wasn't implemented, it'd just return None.

But I want to be clear:  if you ```import chassis2024.argparse```, the ```ARGPARSE``` interface will absolutely definitely be defined -- it'll be defined to that module itself.

Q: "Could you just directly read chassis2024.argparse.args?"

A: Yes, you can.  But one of the goals of the system is to make infrastructure swappable.  You could write a different argparse module, for your special needs.  Perhaps the ordering in your particular execution is really weird, and breaks some of the assumptions that the other infrastructure makes.  You had to make something special.  As long as you implement ```.parser``` and ```.args``` just the same, and declare your new module to meet the ```ARGPARSE``` interface, then the code should still work.  You just need to change the ```import chassis2024.argparse``` to ```import <your-code>.argparse```, or whatever, and it'll work.

Q: "That seems unlikely.  Are you sure you aren't just being pedantic?"

A: Hm, ...  Maybe I am.  But this is how it makes sense to me to think about it.  Do what you like.

### Wait a second!  What about the "words"?!

OK.

This is really basic.

```
from chassis2024.words import *
from chassis2024.argparse.words import *
```

I'll show you what the text of ```chassis2024.words``` looks like, somewhat abbreviated:

```
# Copyright 2024 Lion Kimbro
# SPDX-License-Identifier: BSD-3-Clause

CHASSIS2024_SPEC = "CHASSIS2024_SPEC"
...
INTERFACES = "INTERFACES"
...
# common interfaces
RUN = "RUN"  # basicrun: .run()
ARGPARSE = "ARGPARSE"  # argparse: .parser, .args
PERSISTENCE_DATA = "PERSISTENCE_DATA"  # basicjsonpersistence: .data, .save()
...
# MAJOR STAGES
CLEAR = "CLEAR"
RESET = "RESET"
ARGPARSE = "ARGPARSE"
CONNECT = "CONNECT"
ACTIVATE = "ACTIVATE"
UP = "UP"
...
```

See?  That's all it is.

These variables (RUN, ARGPARSE, PERSISTENCE_DATA) are what I call "words."  (Or to use more technical jargon, these are *"symbols"*, their value is their own name, and the id is fixed in the string interning table.)

I use "words" for three reasons:

* To save two whole characters in dictionary indexing -- it's ```RUN```, rather than ```"RUN"```.  I like it much better as ```RUN```.
* To syntax highlight the common keys as identifiers, rather than as strings, which creates a different impression in my mind.
* *The real reason:*  To detect errors earlier.  If I type "INTERFCES", rather than "INTERFACES", then there will just be a silent but horrifying omission -- "Hm, looks like the user didn't want to define any *INTERFACES* here...  Things won't work, and I'll have to trouble-shoot to find out why.  But if I use the *word* INTERFCES. rather than the *word* INTERFACES, then at import time, Python will say, "Hey, you're talking about an identifier INTERFCES that you haven't defined yet."  So it makes me feel immensely more secure to just define words for my dictionary keys.

*I have met people who don't like any of this.*  They say, "It's Python, it's a dictionary, it's supposed to have string keys..."  "You should use a class and an object and attributes, if you want to do this..."  But then, even if I do, I still have the same problem -- because Python will let you assign to foo.interfces, no problem, ...  ANYWAYS.  If you don't like it, don't import words, and just ignore them.  You can program using just strings for keys if you like, everything will work fine.


### Recap

So, as before, a revisiting of the ```echo.py``` example as a totality:

```
import sys

import chassis2024
import chassis2024.basicrun
import chassis2024.argparse
from chassis2024.words import *
from chassis2024.argparse.words import *


this_module = sys.modules[__name__]


CHASSIS2024_SPEC = {
    INTERFACES: {RUN: this_module,
                 ARGPARSE_CONFIGURE: this_module}
}


# interface: ARGPARSE_CONFIGURE
def argparse_configure(parser):
    parser.add_argument("-e", "--echo",
                        help="input string to echo",
                        default="use -e to specify string to echo")

# interface: RUN
def run():
    argparser = chassis2024.interface(ARGPARSE, required=True)
    print(argparser.args.echo)


if __name__ == "__main__":
    chassis2024.run()
```

* まず、("first off,") we import the ```chassis2024``` system itself.
* Then the infrastructure used: ```chassis2024.basicrun```, and ```chassis2024.argparse```.
* Then words for the modules, since there is specialized language here.
* Then we define the ```CHASSIS2024_SPEC```, and in particular, insisting that RUN and ARGPARSE_CONFIGURE interfaces are implemented by ```echo.py```.
  * And again, I re-emphasize that interfaces can only be implemented by a single module.  This isn't [pluggy.](https://pluggy.readthedocs.io/en/stable/)  This isn't [Zope components.](https://pypi.org/project/zope.component/)  This isn't any kind of [bus](https://en.wikipedia.org/wiki/Software_bus) or component or plug-in system.  It's just a system for sequencing critical infrastructure for setup and teardown.
* Then the ARGPARSE_CONFIGURE interface is implemented.  The parser is configured in this way.
* Then the RUN interface is implemented.
  * The first thing it does, is located the argparser.
  * Then it drills down for the ```args```, and pulls out the ```echo``` argument.
  * Then it prints it.
* And then the ```chassis2024``` system is run.


### Thought Experiments

Feel free to skip, but this can give you some insight into the inner logic behind chassis2024.

#### Thought Experiment #1: Other Infrastructure Registering Arguments

Q: "Hey, can other pieces of infrastructure register themselves on the argument parser?"

A: ... Yes...

Q: "For example, if I made a piece of infrastructure that pulled some data from a remote host and port, it could collect the --host and --port via ```chassis2024.argparse```, right?"

A: ... Yes...

Q: "Why so cagey?  Isn't this exactly what the system was made for?"

A: ...

A: Okay, so, YES, and NO.

Q: ?

A: What I mean is:  YES, you absolutely can do that.  And the system is set up to give you that freedom, to do it.  You can define an execution node, after the argument parser is defined, and before it performs it's parse, and you can automatically register arguments on it, by reaching out to it by interface, but, ...

Q: "-- but what?"

A: It was important to me to make sure that the programmer has ultimate control over how the ArgumentParser presents to the user.  I wanted programmers to be able to use pre-existing infrastructure, and yet not have to compromise on the presentation to the user.  I mean, the user *is* the *programmer's* user, right?  Not necessarily the *infrastructure programmer's* user.  And the ArgumentParser -- because it can display --help, and because the options themselves are defined on it -- I wanted to make sure that that was all in the control of the programmer.

Q: "Oh?"

A: ...but I still wanted the programmer to be able to use "defaults" if they were okay with it.  So I settled on a compromise.

Q: "What was that?"

A: I defined ```argparse_configure(parser)``` in a sensible way on the infrastructure, but I didn't bind that functionality to the execution graph, or to any given interface.  If the programmer wants to do that, the program can absolutely do that, via ```INTERFACES: {ARGPARSE_CONFIGURE: <some_infrastructure_module>}```.  Or the programmer can just manually call (for example:) ```<some_infrastructure_module>.argparse_configure(parser)``` from their own ARGPARSE_CONFIGURE implementation, and get the benefit of the parser registration.  You'll see that in the next example, by the way.

Q: "OK.  So, you *can* do automatic ```parser.add_argument``` registrations, but you made it just slightly less automatic, because you think most programmer's will want to tightly control how the ```ArgumentParser``` is configured."

A: Yeah basically that's it.

Q: "I notice that, because only one interface can implement ARGPARSE_CONFIGURE, that ..."

A: Yeah, only one would be able to do it.

Q: "Isn't that a problem?"

A: Yes?  And I do think about integrating [pluggy](https://pluggy.readthedocs.io/en/stable/) into chassis2025, or chassis2026 -- whenever the next version of chassis might be.  But in another way, I think it's saving our hides.

Q: What do you mean?

A: Well, it depends on Kahn's algorithm.  With a different or rejiggered execution of the scheduler, it might run the argument parsing configuration in a different order.  If the only thing is, "Run this before parsing the arguments," and you had two pieces of infrastructure both wanting to add their parameters to the argument parser, then sometimes you might run it and get the presentation in one order, and other times get the presentation in another order...  Since it's user-facing, I prefer to keep it explicit.  And keeping it explicit means: Just use one single implementation of the ARGPARSE_CONFIGURE interface, and then explicitly lay down the order in which the arguments are added.  Call into the packages manually, and say, "Add your arguments, now!", in a specific order.

Q: If you are going to do everything explicitly, then why did you even set up this system like chassis2024, which is about flexibility?

A: I wanted both.  I wanted to be able to say, "Here are a bunch of pieces of infrastructure, work out how to make them cooperate, time-wise," but I also wanted to be able to clarify, "Here's the order that you should do THESE THINGS in."  I just want to be able to rapidly compose software from parts.  But I also recognize that the steps and promises involved in putting a running system together, and then decomposing the same system, are critically important to the design and success of that system.  And by the way, you CAN fully automate the assembly of arguments in an argument parser, in this system: just build an infrastructure package, have it look through sys.modules at the right time, find infrastructure and find implementations of a particular function, and call it.  It'll work.  I just happen to think that the ArgumentParser is user-facing and thus needs to be treated more delicately.
