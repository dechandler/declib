"""

"""
import argparse
import sys


class DeclibCliPreprocessor:

    def __init__(self, extra_parser_args=None):
        """


        """
        extra_parser_args = extra_parser_args or {}

        self.parser_args = {
            'app_dir': {
                'aliases': ['-d', 'dir_path', 'dir'],
                'type': str,
                'help': "Path to user app directory"
            },
            'config_path': {
                'aliases': ['-c', 'config', 'conf'],
                'type': str,
                'help': "Config file path"
            }
        }
        self.parser_args.update(extra_parser_args)


    def parse_args(self, args=None):

        args = args or sys.argv[1:]

        parser = argparse.ArgumentParser()
        for name, parser_arg in self.parser_args.items():
            matches = [f"--{name}"]
            for alias in parser_arg['aliases']:
                if alias and alias.startswith("-"):
                    matches.append(alias)
                else:
                    matches.append(f"--{alias}")
            parser.add_argument(
                *matches,
                type=(parser_arg.get('type', str)),
                help=parser_arg.get('help', "")
            )

        config_args, self.execution_args = parser.parse_known_args(args=args)
        self.config_args = {
            k: v for k, v in config_args.__dict__.items() if v is not None
        }
        return self.config_args, self.execution_args
