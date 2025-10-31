
import datetime
import logging
import os
import sys

import yaml

log = logging.getLogger("declib")


class DeclibConfig(dict):

    def __init__(self, log, extra_defaults, path_opts):

        super().__init__()

        self.log = log
        self.name = log.name
        self.extra_defaults = extra_defaults
        self.path_opts = path_opts

        self.path, self.config_file_data = self._get_config_file_data()
        self.config_dir = os.path.dirname(self.path)

        # Get config defaults
        self.update(self.get_defaults())

        # TODO: generic interface for merging special config structures

        # Merge general config and set merged loggers value
        self.update(self.config_file_data or {})

        self._expand_paths()

        self.log.configure_loggers(self)


    def _get_config_file_data(self):
        """
        The priority order is:
            Environment variable: APP_NAME_CONFIG (~ accepted)
            $HOME/.config/app-name/config.yaml

        """
        search_paths = [
            os.environ.get(f"{self.name.upper().replace('-', '_')}_CONFIG", ""),
            f"~/.config/{self.name}/config.yaml"
        ]
        for path_var in search_paths:
            path = os.path.expanduser(path_var)
            try:
                with open(path) as fh:
                    config_file_data = yaml.safe_load(fh)
                    self.log('info', f"Config Path: {path}")
                self.path = path
                break
            except FileNotFoundError:
                pass
            except yaml.scanner.ScannerError:
                self.log('error', f"File exists at {path} but is not YAML parseable, aborting...")
                sys.exit(1)
            except Exception as e:
                self.log('debug', ' '.join([
                    "Unexpected exception while loading",
                    f"yaml at {path}: ({e.__class__}) {e}"
                ]))
        else:
            config_file_data = {}
            self.path = path

        return path, config_file_data


    def get_defaults(self):

        defaults = {
            'log_path': f"{self.config_dir}/log/{self.name}.log",
            'log_level': "INFO",
            'stderr_log_level': "WARNING"
        }
        self.path_opts.append('log_path')
        defaults.update(self.extra_defaults)
        return defaults


    def _expand_paths(self):

        def resolve_path(path, default_dir):

            # Resolve ~ to home dir
            path = os.path.expanduser(path)

            # Assume path is relative to default_dir if not abolute
            if not os.path.isabs(path):
                path = os.path.join(self.config_dir, path)

            return path

        for opt in self.path_opts:
            self[opt] = resolve_path(self[opt], self.config_dir)
