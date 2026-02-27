
import json
import os
import sys

import yaml


class DeclibConfig(dict):

    def __init__(self,
        name,
        log,
        config_args=None,
        extra_defaults=None,
        path_opts=None
    ):

        super().__init__()

        self.name = name
        self.log = log
        self.config_args = config_args or {}
        self.extra_defaults = extra_defaults or {}
        self.path_opts = ['config_path', 'app_dir']
        self.path_opts.extend(path_opts or [])

        self.env_stem = self.name.upper().replace('-', '_')


        self['app_dir'] = (
            self.config_args.get('app_dir')
            or os.environ.get(f"{self.env_stem}_APP_DIR")
            or f"~/.config/{self.name}"
        )
        self['config_path'] = self._get_config_path()
        self['config_dir'] = os.path.dirname(self['config_path'])

        config_file_data = self._get_config_file_data()
        if 'app_dir' in config_file_data:
            self['app_dir'] = config_file_data['app_dir']


        # Get config defaults
        self.update(self.get_defaults())

        # TODO: generic interface for merging special config structures

        # Merge general config and set merged loggers value
        self.update(config_file_data or {})

        self._expand_paths()

        self.log.configure_loggers(self)


    def _get_config_path(self):

        config_path = (
            self.config_args.get('config_path')
            or os.environ.get(f"{self.env_stem}_CONFIG_PATH")
            or os.path.join(self['app_dir'], "config.yaml")
        )

        return os.path.expanduser(config_path)


    def _get_config_file_data(self):
        """
        The priority order is:
            Environment variable: APP_NAME_CONFIG (~ accepted)
            $HOME/.config/app-name/config.yaml

        """
        try:
            with open(self['config_path']) as fh:
                config_file_data = yaml.safe_load(fh)
                self.log.info(f"Config Path: {str(self['config_path'])}")
                self.log.debug(json.dumps(config_file_data))

            return config_file_data

        except FileNotFoundError:
            pass
        except yaml.scanner.ScannerError:
            self.log.error(f"File exists at {self['config_path']} but is not YAML parseable, aborting...")
            sys.exit(1)
        except Exception as e:
            print(e.__class__)
            self.log.debug(' '.join([
                "Unexpected exception while loading",
                f"yaml at {self['config_path']}: ({e.__class__}) {e}"
            ]))


        return {}



    def get_defaults(self):

        defaults = {
            'log_path': f"{self['config_dir']}/log/{self.name}.log",
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
                path = os.path.join(self['config_dir'], path)

            return path

        for opt in self.path_opts:
            self[opt] = resolve_path(self.get(opt, ''), self['config_dir'])
