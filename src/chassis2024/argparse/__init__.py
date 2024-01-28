"""basic argument parsing component for chassis2024

Perform argument processing with the python argparse module.


STAGES:
------------------------------------------------------------------------

  <CLEAR>
  + *CLEAR_ARGPARSE   -- Null's .parser, .args
  <RESET>
  + *RESET_ARGPARSE   -- sets .parser to ArgumentParser instance
  <*ARGPARSE>         -- sets .args to .parser.parse_args()

  (key):  <BUILT-IN EXECUTION NODE>
          + CREATED EXECUTION NODE
          *IMPLEMENTED_EXECUTION_NODE
             (executed via this module's
              .perform_execution_graph_node(n) implementation)


INTERFACES IMPLEMENTED:
------------------------------------------------------------------------

  Interface "ARGPARSE":

    .parser  -- an argparse.ArgumentParser
    .args  -- the results of parsing, as returned by argparse.ArgumentParser


INTERFACES CONSUMED:
------------------------------------------------------------------------

  Interface "ARGPARSE_CONFIGURE"

    .argparse_configure(parser)  -- called in RESET_ARGPARSE,
                                    with the newly minted ArgumentParser,
                                    so that the programmer can configure
                                    the parser with ease

CONFIGURATION PROCEDURES:
------------------------------------------------------------------------

  The recommended way to configure the ArgumentParser is to implement
  the ARGPARSE_CONFIGURE interface.  It will be called during
  RESET_ARGPARSE.

  (example, by implementing the ARGPARSE_CONFIGURE interface:)
  ----------------------------------------------------------------------
  import chassis2024.argparse
  ...

  this_module = sys.modules[__name__]
  CHASSIS2024_SPEC = {
      INTERFACES: {ARGPARSE_CONFIGURE: this_module},
      ...
  }

  def argparse_configure(parser):
      parser.add_argument("-e", "--echo",
                          help="input string to echo",
                          default="use -e to specify string to echo")
  ----------------------------------------------------------------------

  Another way is to access the ARGPARSE interface and manipulate the
  .parser manually.  This must be done between RESET_ARGPARSE and
  <ARGPARSE>, if you are going to do it that way.


CONFIGURATION PROCEDURES (OTHER COMPONENT PACKAGES):
------------------------------------------------------------------------

  A special note about component packages, that want to supply
  arguments to the user:

  Component packages should supply functions for extending the argument
  parser that look like so:

  ----------------------------------------------------------------------
  def argparse_configure(parser, default_port=8000):
      group = parser.add_argument_group("Hosting",
                                        "Configure host & port")
      group.add_argument("-h", "--host",
                         help="host domain name or IPv4 address",
                         default="127.0.0.1")
      group.add_argument("-p", "--port",
                         help="port assignment",
                         type=int,
                         default=default_port)
  ----------------------------------------------------------------------

  Only ONE chassis2024 module specification can authoritatively
  implement the ARGPARSE_CONFIGURE interface (that defines
  argparse_configure(parser)), so you will likely call
  argparse_configure manually on component modules, in the order that
  you want them to contribute their arguments, and with your chosen
  default values.

  This is deliberate, it is not an unfortunate accident: I want to be
  sure that the order in which arguments are added to the
  ArgumentParser is fully controlled by the programmer, and I want to
  be sure that the ArgumentParser itself is only touched by the
  programmer -- that nothing is added to it automatically, by other
  components.


USE PROCEDURES:
------------------------------------------------------------------------

  (by way of example:)
  ----------------------------------------------------------------------
  argparser = chassis2024.interface(ARGPARSE, required=True)
  print(argparser.args.echo)
  ----------------------------------------------------------------------
"""

import sys
import argparse


import chassis2024
from chassis2024.words import *

from .words import *


CHASSIS2024_SPEC = {
    EXECUTES_GRAPH_NODES: [CLEAR_ARGPARSE, RESET_ARGPARSE, ARGPARSE],
    EXECUTION_GRAPH_SEQUENCES: [(CLEAR, CLEAR_ARGPARSE, RESET, RESET_ARGPARSE, ARGPARSE)],
    INTERFACES: {"ARGPARSE": sys.modules[__name__]}
}


# globals

parser = None
args = None


# entry

def perform_execution_graph_node(n):
    global parser, args
    
    if n == CLEAR_ARGPARSE:
        parser = None
        args = None
    
    elif n == RESET_ARGPARSE:
        parser = argparse.ArgumentParser()
        args = None
        module = chassis2024.interface(ARGPARSE_CONFIGURE)
        if module is not None:
            module.argparse_configure(parser)
    
    elif n == ARGPARSE:
        args = parser.parse_args()

