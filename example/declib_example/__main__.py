#!/usr/bin/env python3
"""


"""
import logging
import os
import sys

from .cli import ExampleCli
from .config import ExampleConfig
from .exceptions import ExampleException


# Use the app's name here
log = logging.getLogger("declib-example")


def _main():

    # Load custom configuration object
    # Continue, or go to $REPO/declib/example/declib_example/config.py 
    #   for further details on the Config object
    config = ExampleConfig()

    # Log things!
    log.info("Declib Example Run")
    log.debug(f"  PID: {os.getpid()}")
    log.debug(f"  Args: {sys.argv[1:]}")

    # Execute the main CLI handler
    # Go to $REPO/declib/example/declib_example/cli/main.py
    ExampleCli(config).handle_args(sys.argv[1:])


def main():
    # Wrap the real main call in a try/except to catch stray
    # exceptions and exit gracefully
    try:
        _main()
    except (
        ExampleException,
        KeyboardInterrupt
    ) as e:
        log.error(f"Exiting due to {e.__class__}: {str(e)}")
