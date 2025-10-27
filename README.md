# DEClib

Simple framework for CLI applications


## How to Use

The example environment in `example/`, invoked by `example.py`, is thoroughly commented and covers usage. Formal documentation should come later.

In your package's `__main__.py`, import your DeclibLogger, DeclibConfig
and DeclibCli classes, then pass them into an invocation of DeclibMain

The cli workflow is subcommand-oriented, operating by consuming arguments from the left to choose execution paths. Subcategories of commands are contained in other DeclibCli classes.
