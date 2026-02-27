# DEClib

A lightweight Python framework for building subcommand-driven CLI applications.

---

### Description

DEClib provides a thin, opinionated scaffold for CLI tools. Rather than prescribing application logic, it wires together the plumbing that every CLI app needs (argument parsing, configuration loading, and logging) and gets out of the way. The framework is built around inheritance: each component (config, CLI router, API layer, logger) is a base class you subclass and extend for your own application.

The result is a consistent, predictable structure across projects without locking you into a heavy framework.

---

### Functionality

#### `DeclibMain`

The entry point. Instantiate it in your `__main__.py`, passing in your subclasses of the logger, config, and CLI objects. It handles the startup sequence: preprocessing raw CLI arguments to separate config flags from execution arguments, initializing the config and logger, and routing execution to the CLI handler.

```python
from declib import DeclibMain, DeclibLogger
from .cli import ExampleCli
from .config import ExampleConfig

def main():
    DeclibMain(DeclibLogger, ExampleConfig, ExampleCli)
```

#### `DeclibCli`

The CLI router. Subcommands are registered in a `self.operations` dict, where each key is a command name and the value defines the handler, optional aliases, and a help string. Routing consumes arguments from the left - the first argument selects an operation, and the remainder are passed along for further handling. Subcategories of commands can be nested into their own `DeclibCli` subclasses, enabling arbitrarily deep command trees.

```python
self.operations = {
    'run': {
        'handler': self.run,
        'aliases': ['r'],
        'help': "Run the main operation"
    },
    'sub': {
        'handler': lambda: SubCli(self.config),
        'help': "Enter the sub-command group"
    }
}
```

When no arguments are given, the router falls back to a `no_args_operation` (default: `help`). When an argument doesn't match any registered operation, it falls back to a `no_matching_args_operation` (default: `print`). Both defaults are overridable. A `help` command is always available implicitly, and auto-generates a listing from `self.operations` if no custom `help_message` is set.

Custom pre-routing logic can be injected by overriding `extra_arg_checks()`.

#### `DeclibConfig`

A `dict` subclass that assembles application configuration from three sources in priority order:

- CLI flags (`--app_dir`, `--config_path`, and any extras you register)
- Environment variables (auto-derived from your app name, e.g. `MYAPP_CONFIG_PATH`)
- A YAML config file (defaults to `~/.config/<app-name>/config.yaml`)

Subclass it to define application-specific defaults and path options. Values declared in `path_opts` are automatically resolved to absolute paths, expanding `~` and handling paths relative to the config file's directory.

```python
class ExampleConfig(DeclibConfig):
    def __init__(self, log):
        extra_defaults = {
            'stuff': 'things',
            'place': '~/tmp/blah'
        }
        path_opts = ['place']
        super().__init__(log, "my-app", extra_defaults, path_opts)
```

#### `DeclibLogger`

A wrapper around Python's standard `logging` module that solves the bootstrap problem - log calls made before configuration is complete are buffered and replayed once the file and stderr handlers are set up. After configuration, messages are routed to both a rotating file log and stderr, each with independently configurable levels (`log_level` and `stderr_log_level` in config).

Convenience methods (`log.debug()`, `log.info()`, `log.warn()`, `log.error()`, etc.) are available directly on the logger instance.

#### `DeclibApi`

A base class for the layer that holds your application's actual logic. Separating API from CLI means your application can be imported and used programmatically or wired to other interfaces without coupling to the command-line layer.

Includes a `run_command()` utility for executing OS subprocesses with concurrent stdout/stderr stream handling, optional passthrough printing, and log capture. ANSI escape codes are stripped from captured output.

#### `DeclibCliPreprocessor`

Separates config-level flags from execution arguments before the main CLI router sees them. Built on `argparse`, it handles `--app_dir` and `--config_path` by default. Additional flags can be registered by passing `extra_parser_args` to `DeclibMain`. Known flags are consumed; everything else is passed on as execution arguments.

---

### Utilities

#### `DeepAddressableDictlike`

A nested dict wrapper with dot-notation path addressing. Supports `get`, `set`, `update`, and iteration using either period-delimited strings (`"section.subsection.key"`) or lists as path addresses. Useful for working with deeply nested configuration or data structures without chaining bracket lookups.

```python
d = DeepAddressableDictlike()
d.set("section.key", "value")
d.get("section.key")  # -> "value"
d["section.key"]      # -> "value"
```

#### `MarkYamlDataLoader`

Parses a "MarkYaml" format, where Markdown-style `#` headers are used as structural keys, with content blocks between headers parsed as YAML. This allows structured data documents to be ergonomically written in a Markdown editor while still being machine-readable.

Headers prefixed with `- ` render their children as a list rather than a dict, and lines starting with `//` are ignored as comments.

```python
data = MarkYamlDataLoader("data.md").data
```

---

### Installation

```bash
./build.sh
pip install dist/declib-0.0.1-py3-none-any.whl
```

Requires Python > 3.8. The only dependency is `pyyaml`.

---

### Usage

#### Minimal app structure

```
my-app/
    __init__.py
    __main__.py
    api.py
    cli.py
    config.py
    exceptions.py
```

#### `__main__.py`

```python
from declib import DeclibMain, DeclibLogger
from .cli import MyCli
from .config import MyConfig
from .exceptions import MyException
import logging

log = logging.getLogger("my-app")

def main():
    try:
        DeclibMain(DeclibLogger, MyConfig, MyCli)
    except (MyException, KeyboardInterrupt) as e:
        log.error(f"Exiting: {e}")
```

#### `config.py`

```python
from declib import DeclibConfig

class MyConfig(DeclibConfig):
    def __init__(self, log):
        super().__init__(log, "my-app",
            extra_defaults={'output_dir': '~/my-app/output'},
            path_opts=['output_dir']
        )
```

#### `cli/main.py`

The top-level CLI router. Operations can delegate to methods on the class or hand off to a nested `DeclibCli` subclass via a lambda.

```python
from declib import DeclibCli
from .run import RunCli

class MyCli(DeclibCli):
    def __init__(self, config):
        super().__init__(config)
        self.operations = {
            'dump-config': {
                'aliases': ['d', 'dump'],
                'handler': self.dump_config,
                'help': "Dump running config"
            },
            'run': {
                'aliases': ['r'],
                'handler': lambda: RunCli(self.config).handle_args,
                'help': "Subcommand for running things"
            }
        }
        self.no_args_operation = 'help'
        self.no_matching_args_operation = 'run'

    def dump_config(self, args):
        import json
        print(json.dumps({**self.config}, indent=4))
```

#### `cli/run.py`

A nested CLI router - its operations are only reachable after `run` (or an alias) is consumed from the argument list.

```python
from declib import DeclibCli
from ..api import MyApi

class RunCli(DeclibCli):
    def __init__(self, config):
        super().__init__(config)
        self.operations = {
            'task': {
                'aliases': ['t'],
                'handler': self.run_task,
                'help': "Run the main task"
            }
        }

    def run_task(self, args):
        MyApi(self.config).do_something()
```

#### `api.py`

```python
from declib import DeclibApi

class MyApi(DeclibApi):
    def __init__(self, config):
        super().__init__(config)

    def do_something(self):
        self.log.info("Doing something")

        # Default - streams print live and are logged
        stdout, stderr = self.run_command(['ss', '-plnt'])

        # Capture quietly, then handle output yourself
        stdout, stderr = self.run_command(
            ['cat', '/etc/issue'],
            print_stdout=False, log_stdout=False,
            print_stderr=False, log_stderr=False
        )

        # Set a working directory
        self.run_command(['pwd'], cwd='/tmp')

        # Pipe text into stdin
        self.run_command(['grep', 'pattern'], stdin='line one\nline two\n')
```

#### Invocation

```bash
# Run directly
python -m my-app run

# With config override
python -m my-app --config_path /path/to/config.yaml run

# With app dir override
python -m my-app --app_dir /path/to/appdir run

# Get help
python -m my-app help
```

---

### Configuration file

DEClib looks for a YAML config file at `~/.config/<app-name>/config.yaml` by default. Config values set here are merged with defaults, with the file taking precedence. Path values are resolved relative to the config file's directory.

```yaml
# ~/.config/my-app/config.yaml
log_level: DEBUG
stderr_log_level: WARNING
output_dir: ~/my-app/output
```

Built-in config keys:

- `app_dir` - base directory for app data (default: `~/.config/<app-name>`)
- `config_path` - path to the config file
- `log_path` - path to the log file (default: `<config_dir>/log/<app-name>.log`)
- `log_level` - file log level (default: `INFO`)
- `stderr_log_level` - stderr log level (default: `WARNING`)

Config values can also be set via environment variables. The variable names are derived from your app name by uppercasing it and replacing hyphens with underscores - for example, for an app named `my-app`, the config path variable would be `MY_APP_CONFIG_PATH`.

---

### Intent

DEClib is designed for developers who want to write clean, maintainable CLI tools without reaching for a heavy framework. It favors explicit subclassing over decorators and convention over magic, keeping the startup flow easy to trace and the components easy to replace. The class-based architecture means each layer (CLI, config, API, logging) can be extended or swapped independently as a project grows.
