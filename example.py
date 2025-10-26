#!/usr/bin/env python3
"""
This runs a dummy application to demonstrate and document
declib's usage and capabilities

Follow the execution path for full coverage

"""
import os
import sys

# Below we're adding the declib repo source directory to
#   our Python PATH, so no setup is required for the demo.
# Declib should be installed in your app environment, so
#   this won't be necessary in other contexts
example_src_dir = os.path.abspath(os.path.join(__file__, "../example"))
sys.path.append(example_src_dir) if example_src_dir not in sys.path else None


# Execute app's main function
from declib_example.__main__ import main
main()

# Go to $REPO/example/declib_example/__main__.py
