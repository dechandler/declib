"""

"""
import os
import sys


class DeclibMain:

    def __init__(self, Logger, Config, Cli):

        log = Logger()

        # Load custom configuration object
        # Continue, or go to $REPO/declib/example/declib_example/config.py 
        #   for further details on the Config object
        config = Config(log)

        # Log things!
        log.info(f"Running {config.name}")
        log.debug(f"  PID: {os.getpid()}")
        log.debug(f"  Args: {sys.argv[1:]}")

        # Execute the main CLI handler
        # Go to $REPO/declib/example/declib_example/cli/main.py
        Cli(config).handle_args(sys.argv[1:])
