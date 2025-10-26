"""


"""
import logging
import os
import sys

# declib source dir in Python PATH - you won't need to do this
declib_src_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.append(declib_src_dir) if declib_src_dir not in sys.path else None

from declib import DeclibApi


log = logging.getLogger("declib-example")


class ExampleApi(DeclibApi):
    """
    DeclibApi objects are what provide the interface to underlying functionality

    This is so that the app can be imported and used elsewhere or used
    with interfaces other than the cli

    """


    def __init__(self, config):

        super().__init__(config)

    def demo_run_command(self):
        # DeclibApi provides a .run_command() method that returns and
        # optionally prints or logs the command's stdout and stdin (all on
        # by default)
        self.run_command(['ss', '-plnt'])


    def demo_silent(self):

        # DeclibApi also returns stdout and stderr, so you can turn off
        # default outputs

        stdout, stderr = self.run_command(
            ['cat', '/etc/issue'],
            print_stdout=False, log_stdout=False,
            print_stderr=False, log_stderr=False
        )
        print("Command complete")
        print("Stdout lines:")
        print(stdout)
        print("Stderr lines:")
        print(stderr)


    def demo_cwd(self, cwd):

        # Specify working directory for a command
        self.run_command(['pwd'], cwd=cwd)

    def demo_stdin(self, stdin):

        # To pipe something into stdin
        self.run_command(['grep', 'a'], stdin=stdin)
