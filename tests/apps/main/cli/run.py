"""

"""
import json
import os
import sys

# declib source dir in Python PATH - you won't need to do this
declib_src_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.append(declib_src_dir) if declib_src_dir not in sys.path else None

from declib import DeclibCli

from ..api import ExampleApi


class ExampleRunCli(DeclibCli):

    def __init__(self, config):
        """

        """
        super().__init__(config)

        self.operations = {
            'demo_run_command': {
                'aliases': ['cmd', 'run', 'run_cmd'],
                'handler': self.demo_run_command,
                'help': "Run `ss -plnt` to demonstrate vanilla command run"
            },
            'demo_silent': {
                'aliases': ['silent', 's', 'quiet', 'q'],
                'handler': self.demo_silent,
                'help': "Run `cat /etc/issue`, save output and print after complete"
            },
            'demo_cwd': {
                'aliases': ['cwd'],
                'handler': self.demo_cwd,
                'help': "Run `pwd` with current working directory set"
            },
            'demo_stdin': {
                'aliases': ['in', 'stdin'],
                'handler': self.demo_stdin,
                'help': "Run `grep` against a multiline input string"
            }
        }


    def demo_run_command(self, args):

        # To keep the CLI a dumb execution path layer, the API
        #   handles backend actions
        api = ExampleApi(self.config)

        # DeclibApi provides a .run_command() method that returns and
        # optionally prints or logs the command's stdout and stdin (all on
        # by default)
        stdout, stderr = api.run_command(['ss', '-plnt'])


    def demo_silent(self, args):

        # DeclibApi also returns stdout and stderr, so you can turn off
        # default outputs
        api = ExampleApi(self.config)
        stdout, stderr = api.run_command(
            ['cat', '/etc/issue'],
            print_stdout=False, log_stdout=False,
            print_stderr=False, log_stderr=False
        )
        print("Command complete")
        print("Stdout lines:")
        print(stdout)
        print("Stderr lines:")
        print(stderr)


    def demo_cwd(self, args):

        # Specify working directory for a command
        api = ExampleApi(self.config)
        api.run_command(['pwd'], cwd="/dev/shm")


    def demo_stdin(self, args):

        # To pipe something into stdin
        api = ExampleApi(self.config)
        api.run_command(
            ['grep', 'a'],
            stdin='\n'.join([
                "Stuff and Things.",
                "Spam & Eggs.",
                "Grr. Arg."
            ])
        )
