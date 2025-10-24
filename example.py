#!/usr/bin/env python3
"""


"""
import json
import logging
import os
import sys

from declib import (
    DeclibConfig, DeclibCli, DeclibApi
)

# Use the app's name here
log = logging.getLogger("declib-example")


class ExampleConfig(DeclibConfig):

    def __init__(self):

        # These are defaults for config options the app is adding
        extra_defaults = {
            'stuff': 'things',
            'spam': 'eggs',
            'place': '~/tmp/blah'
        }
        # These get handled and expanded as path names
        path_opts = ['place']

        super().__init__("declib-example", extra_defaults, path_opts)


class ExampleCli(DeclibCli):

    def __init__(self, config):
        """
        The basic functionality of a DeclibCli is to handle one arg at
        a time. Each option has a handler, which is passed the remaining
        aruments. It's designed for easy cli argument shorthands.

        """
        super().__init__(config)

        self.operations = {

            'dump-config': {
                # Aliases provide shorthand options that will match
                # this operation
                'aliases': ['d', 'dump', 'dump_config'],

                # This method or function is run when the operation
                # is selected
                'handler': self.dump_config,

                # The default help handler uses this description
                'help': "Dump running config"
            },

            'run': {
                'aliases': ['r'],

                # lambda handlers get unwrapped, so no more class instances
                # are created than are needed
                'handler': lambda: ExampleRunCli(self.config).handle_args,

                'help': "Run something in a submenu"
            }

            # A `help` operation is implied, which by default has a handler
            # `self.print_help`, which in DeclibCli's provided method
            # prints a summary of available operations
        }

        # If there are no arguments at this level, set the default
        self.no_args_operation = 'help'

        # If there are more arguments, but they don't match any defined
        # operations or aliases. This is lazy shorthand 
        self.no_matching_args_operation = 'run'


    def dump_config(self, args):
        """
        Prints the synthesized run config

        Args:
            args (list): Remaining arguments after the current arg is popped

        """
        print(json.dumps({**self.config}, indent=4))


class ExampleRunCli(DeclibCli):

    def __init__(self, config):
        """

        """
        super().__init__(config)

        self.operations = {
            'show_cwd_function': {
                'aliases': ['cwd'],
                'handler': self.show_cwd_function,
                'help': "Run `ls /`"
            },
            'show_stdin_function': {
                'aliases': ['in', 'stdin'],
                'handler': self.show_stdin_function,
                'help': "Run a grep against a multiline input string"
            }
        }
        self.no_args_operation = 'good'


    def show_cwd_function(self, args):

        api = ExampleApi(self.config)
        api.show_cwd_function("/")

    def show_stdin_function(self, args):

        api = ExampleApi(self.config)
        api.show_stdin('\n'.join([
            "Stuff and Things.",
            "Spam & Eggs.",
            "Grr. Arg."
        ]))


class ExampleApi(DeclibApi):
    """
    DeclibApi objects are what provide the interface to underlying functionality

    This is so that the app can be imported and used elsewhere or used
    with interfaces other than the cli

    """


    def __init__(self, config):

        super().__init__(config)

    def show_run_command(self):
        # DeclibApi provides a .run_command() method that returns and
        # optionally prints or logs the command's stdout and stdin (all on
        # by default)
        self.run_command(['ss', '-plnt'])


    def show_run_command_silently(self):

        # DeclibApi also returns stdout and stderr, so you can turn off
        # default outputs

        stdout, stderr = self.run_command(
            ['cat', '/etc/issue'],
            print_stdout=False, log_stdout=False,
            print_stderr=False, log_stderr=False
        )
        print("Command complete")
        print("Stdout:")
        print(stdout)
        print("Stderr:")
        print(stderr)


    def show_cwd_function(self, cwd):

        # Specify working directory for a command
        self.run_command(['ls', './'], cwd=cwd)

    def show_stdin(self, stdin):

        # To pipe something into stdin
        self.run_command(['grep', 'a'], stdin=stdin)


def main():

    config = ExampleConfig()

    log.info("Declib Example Run")
    log.debug(f"  PID: {os.getpid()}")
    log.debug(f"  Args: {sys.argv[1:]}")

    ExampleCli(config).handle_args(sys.argv[1:])


if __name__ == "__main__":

    try:
        main()
    except (
        KeyboardInterrupt
    ) as e:
        log.error(f"Exiting due to {e.__class__}: {str(e)}")
