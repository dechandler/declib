"""


"""
import os
import sys

# declib source dir in Python PATH - you won't need to do this
declib_src_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.append(declib_src_dir) if declib_src_dir not in sys.path else None

from declib import DeclibApi


class ExampleApi(DeclibApi):
    """
    DeclibApi objects are what provide the interface to underlying functionality

    This is so that the app can be imported and used elsewhere or used
    with interfaces other than the cli

    """
    def __init__(self, config):

        super().__init__(config)
