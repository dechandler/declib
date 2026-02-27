"""

"""
import json
import os
import sys

# declib source dir in Python PATH - you won't need to do this
declib_src_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.append(declib_src_dir) if declib_src_dir not in sys.path else None

from declib import DeclibCli

from .run import ExampleRunCli


class ExampleCli(DeclibCli):

    def __init__(self, config):
        """
        The basic functionality of a DeclibCli is to handle one arg at
        a time. Each option has a handler, which is passed the remaining
        aruments. It's designed for arbitrary nesting of subcommands
        and easy cli argument shorthands

        """
        super().__init__(config)

        # .operations defines the options available in this subcommand
        #   along with their convenience shorthands, handler functions, and
        #   a description of the option for generating help output
        self.operations = {

            'dump-config': {
                # Aliases provide shorthand options that will match
                # this operation
                'aliases': ['d', 'dump', 'dump_config'],

                # This method or function is run when the operation
                # is selected, passed the remaining arguments after
                # popping the current subcommand
                'handler': self.dump_config,

                # The default help handler uses this description
                'help': "Dump running config"
            },

            'run': {
                'aliases': ['r'],

                # lambda handlers get unwrapped, so no more class instances
                # are created than are needed
                'handler': lambda: ExampleRunCli(self.config).handle_args,

                'help': "Subcommand for running things"
            }

            # A `help` operation is implied, which by default has a handler
            # `self.print_help`, which in DeclibCli's provided method
            # prints a summary of available operations
        }

        # If there are no arguments at this level, set the default
        self.no_args_operation = 'help'

        # If there are more arguments, but they don't match any defined
        # operations or aliases
        self.no_matching_args_operation = 'run'


    def dump_config(self, args):
        """
        Prints the synthesized run config

        Args:
            args (list): Remaining arguments after the current arg is popped

        """
        print(json.dumps({**self.config}, indent=4))
