

### An Example: pygame infrastructure

This time, instead of *making use of* infrastructure, we're going to be *writing* infrastructure.

I was trying to think of a fun example, and: *pygame* came to mind.  Everybody loves pygame.  Why not make pygame infrastructure?

### Brainstorming the Pygame Infrastructure

The first question is, what should it do?

* It should start pygame.  When the program is running, that is: when the program gets to the "UP" execution node, there should already be a pygame display, all set up, and ready for user interaction.
* It should be configurable.
  * The display resolution should be expressible through the execution spec.
  * Any arbitrary configuration that a programmer could do, should be possible -- that means, an interface must be made available.
* It should be possible to automatically set up the joystick, if that's what the programmer wants.  That suggests another piece of layerable infrastructure.
* It should automatically supply a run loop.  When the QUIT event happens, it gets out of that run loop.
* Of course, it should clean up after itself.  That means adding an automatic call to pygame.quit().  That'll take a single line of code to add.

### Planning

OK, so right away, here's what it looks like, in the terms of chassis2024:

Conventions for the execution spec:
* ```PYGAME``` -- this will be the root key, for configuration of the pygame infrastructure
  * ```WIDTH``` -- this'll be the integer width of the window in pixels (pygame.display.set_mode)
  * ```HEIGHT``` -- this'll be the integer height of the window in pixels (pygame.display.set_mode)
  * ```TITLE``` -- this'll be the text of the window's title (pygame.display.set_caption)
 
New execution Nodes:
* ```ACTIVATE_PYGAME``` -- this'll call pygame.init(), and it'll call pygame.display.set_mode, and pygame.display.set_caption; it'll also set up deferred callback to pygame.quit()
* ```CONFIGURE_PYGAME``` -- this'll be a spot for a programmer to apply arbitrary pygame configuration steps
* ```CONFIGURE_PYGAME_JOYSTICK``` -- this will be a play where joystick setup code can be applied automatically, should that infrastructure be imported

The existing "UP" execution node will be controlled by the pygame infrastructure.  It'll make a main loop that receives events, and give the programmer a crack at them.  It'll also handle the QUIT event, by breaking the main loop.  It'll also call pygame.display.update() between frames.

New interfaces:
* ```RUN``` -- this'll give access to the consumer of the pygame infrastructure
  * ```.pygame_configure()``` -- this will be called during CONFIGURE_PYGAME, so that the user can make custom adjustments
  * ```.pygame_update()```  -- this code will be called once per frame
  * ```.pygame_event(evt)``` -- this code will be called once per event
 
So basically, from the perspective of the programmer making use of the pygame infrastructure, that programmer will do the following:
* ```import pygame_chassis```
* ```from pygame_chassis.words import *```
* ```CHASSIS2024_SPEC = {INTERFACES: {RUN: this_module}, ...}```
* ```EXECUTION_SPEC = {PYGAME: {WIDTH: 640, HEIGHT: 480, TITLE: "a title"}, ...}```
* ```def pygame_configure(): ...```
* ```def pygame_update(): ...```
* ```def pygame_event(): ...```

### First Draft

```
import sys

import chassis2024
import chassis2024.basicrun
import chassis2024.argparse
import chassis2024.basicjsonpersistence
from chassis2024.words import *
from chassis2024.argparse.words import *
from chassis2024.basicjsonpersistence.words import *


this_module = sys.modules[__name__]


CHASSIS2024_SPEC = {
    INTERFACES: {RUN: this_module,
                 ARGPARSE_CONFIGURE: this_module}
}

EXECUTION_SPEC = {
    BASICJSONPERSISTENCE: {
        SAVE_AT_EXIT: True,
        CREATE_FOLDER: False,
        FILEPATH: "./echo_persistence_data.json"
    }
}


# interface: ARGPARSE_CONFIGURE
def argparse_configure(parser):
    parser.add_argument("-e", "--echo",
                        help="input string to echo",
                        default=None)
    parser.add_argument("-r", "--repeat-last",
                        dest="repeat",
                        help="repeat the last used echo string",
                        action="store_true")
    chassis2024.basicjsonpersistence.argparse_configure(parser)

# interface: RUN
def run():
    argparser = chassis2024.interface(ARGPARSE, required=True)
    D = chassis2024.interface(PERSISTENCE_DATA, required=True).data()
    if argparser.args.echo is not None:
        print(argparser.args.echo)
        D["msg"] = argparser.args.echo  # saved automatically
    else:
        print(D.get("msg", "use -e to specify string to echo"))


if __name__ == "__main__":
    chassis2024.run(EXECUTION_SPEC)
```

