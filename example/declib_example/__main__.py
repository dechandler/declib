#!/usr/bin/env python3
"""


"""
import logging
import os
import sys

from declib import (DeclibMain, DeclibLogger)

from .cli import ExampleCli
from .config import ExampleConfig
#from .logging import ExampleLogger
from .exceptions import ExampleException


# Use the app's name here
log = logging.getLogger("declib-example")


def main():

    # Wrap main to catch stray exceptions and exit gracefully
    try:
        DeclibMain(DeclibLogger, ExampleConfig, ExampleCli)
    except (
        ExampleException,
        KeyboardInterrupt
    ) as e:
        log.error(f"Exiting due to {e.__class__}: {str(e)}")
