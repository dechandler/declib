"""

"""
import os
import sys

from .logging import DeclibLogger
from .config import DeclibConfig
from .cli import DeclibCli
from .cli_preprocessor import DeclibCliPreprocessor

class DeclibMain:

    def __init__(self,
        name,
        extra_parser_args=None,
        Logger=DeclibLogger,
        CliPreprocessor=DeclibCliPreprocessor,
        Config=DeclibConfig,
        Cli=DeclibCli
    ):
        """


        """
        log = Logger()

        cli_pre = CliPreprocessor(extra_parser_args)
        config_args, execution_args = cli_pre.parse_args()

        # Load custom configuration object
        # Continue, or go to $REPO/declib/example/declib_example/config.py 
        #   for further details on the Config object
        config = Config(
            name,
            log,
            config_args=config_args
        )

        # Log things!
        log.info(f"Running {config.name}")
        log.debug(f"  PID: {os.getpid()}")
        log.debug(f"  Args: {sys.argv[1:]}")

        # Execute the main CLI handler
        # Go to $REPO/declib/example/declib_example/cli/main.py
        Cli(config).handle_args(execution_args)
