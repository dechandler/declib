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

log = logging.getLogger("example")
out = logging.getLogger("example-stdout")
err = logging.getLogger("example-stderr")

class ExampleConfig(DeclibConfig):

    def __init__(self):

        extra_defaults = {
            'stuff': 'things',
            'spam': 'eggs',
            'place': '~/tmp/blah'
        }
        path_opts = ['place']

        super().__init__("the-thing", extra_defaults, path_opts)


class ExampleCli(DeclibCli):

    def __init__(self, config):
        """


        """
        super().__init__(config)

        self.operations = {
            'run': {
                'aliases': ['r'],
                'handler': lambda: ExampleRunCli(self.config).handle_args,
                'help': "Run the thing"
            },
            'dump-config': {
                'aliases': ['d', 'dump', 'dump_config'],
                'handler': self.dump_config,
                'help': "Dump running config"
            }
        }

    def dump_config(self, args):

        print({**self.config})


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

    def __init__(self, config):

        super().__init__(config)

    def show_cwd_function(self, cwd):

        self.run_command(['ls', './'], cwd=cwd)

    def show_stdin(self, stdin):

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
