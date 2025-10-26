"""


"""
import logging
import os
import sys

# declib source dir in Python PATH - you won't need to do this
declib_src_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.append(declib_src_dir) if declib_src_dir not in sys.path else None

from declib import DeclibConfig


log = logging.getLogger("declib-example")


class ExampleConfig(DeclibConfig):
    """
    The config object sets defaults, loads a config file, and
    configures logging.

    It then gets passed into other objects' __init__s, though
    in most of those cases, a dictionary with needed config
    options will suffice

    """
    def __init__(self):

        # These are defaults for config options the app is adding
        extra_defaults = {
            'stuff': 'things',
            'spam': 'eggs',
            'place': '~/tmp/blah'
        }
        # These values are read as paths and expanded
        #   to absolute paths (expanduser, or relative
        #   to config file)
        path_opts = ['place']

        # Invoke DeclibConfig.__init__() with the prepared values 
        super().__init__("declib-example", extra_defaults, path_opts)
