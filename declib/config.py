
import datetime
import logging
import os
import sys

import yaml

log = logging.getLogger("declib")


class DeclibConfig:

    def __init__(self, app_name, extra_defaults, path_opts):

        self.name = app_name
        self.extra_defaults = extra_defaults
        self.path_opts = path_opts

        self._pre_log = []
        self.log = self.pre_log
        self.log('debug', f"Starting {self.name}")

        self.path, self.config_file_data = self._get_config_file_data()
        self.config_dir = os.path.dirname(self.path)

        # Get config defaults
        self.config = self.get_defaults()

        # TODO: generic interface for merging special config structures

        # Merge general config and set merged loggers value
        self.config.update(self.config_file_data or {})

        self._expand_paths()

        self.configure_loggers()



    def configure_loggers(self):

        # Configure root logger for stderr output
        rootLogger = logging.getLogger()
        rootLogger.setLevel(
            getattr(logging, self.config['stderr_log_level'].upper())
        )
        handler = logging.StreamHandler(stream=sys.stderr)
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        rootLogger.addHandler(handler)

        # Configure app file log
        appLogger = logging.getLogger(self.name)
        appLogger.setLevel(
            getattr(logging, self.config['log_level'].upper())
        )
        os.makedirs(os.path.dirname(self.config['log_path']), exist_ok=True)

        handler = logging.FileHandler(self.config['log_path'])
        msgfmt = "%(asctime)s (%(process)d) %(levelname)-7s: %(message)s"
        datefmt = "%Y-%m-%d_%H:%M:%S"
        handler.setFormatter(logging.Formatter(msgfmt, datefmt=datefmt))
        appLogger.addHandler(handler)

        # Connect declib logging to file log and flush saved entries
        log.addHandler(handler)
        self.log = self.full_log
        self.flush_pre_log()

        self.stderr_logger = rootLogger
        self.file_logger = appLogger


    def pre_log(self, level, message):
        """
        Since this object is created and begins generating logs
        before logging is configured, stash log messages for
        later replay into the correct log

        """
        # Prepend timestamp to message, since this will be replayed later
        message = f"{datetime.datetime.now().strftime("%H:%M:%S")} {message}"

        self._pre_log.append((level, message))

    def full_log(self, level, message):
        """
        This is a passthrough method to fit the pre_log interface
        but write directly to the log, so that the log interface
        can be consistent in this class

        """
        log.log(logging.__dict__[level.upper()], message)

    def flush_pre_log(self):

        # Refuse to flush if log has not been configured
        if self.log is self.pre_log:
            return

        # Empty self._pre_log into the updated log method
        for level, message in self._pre_log:
            self.log(level, message)
        self._pre_log = []


    def __getitem__(self, key):
        return self.config[key]

    def get(self, key, default):
        return self.config.get(key, default)


    def items(self):
        return self.config.items()

    def keys(self):
        return self.config.keys()

    def values(self):
        return self.config.values()


    def __setitem__(self, key, value):
        self.config[key] = value

    def update(self, update_data):
        self.config.update(update_data)

    def __delitem__(self, key):
        try:
            del self.config[key]
        except KeyError:
            pass

    def _get_config_file_data(self):
        """
        The priority order is:
            Environment variable: SYSTOGONY_CONFIG (~ accepted)
            $HOME/.config/systogony/config.yaml

        """
        search_paths = [
            os.environ.get(f"{self.name.upper().replace('-', '_')}_CONFIG", ""),
            f"~/.config/{self.name}/config.yaml",
            os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), "config.yaml")
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
            self.config[opt] = resolve_path(self.config[opt], self.config_dir)
