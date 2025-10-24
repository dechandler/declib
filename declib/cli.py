
import logging

log = logging.getLogger('declib')



class DeclibCli:

    def __init__(self, config):

        log.debug(f"Initializing {str(self.__class__)}")

        self.config = config

        self.operations = {}

        self.no_args_operation = 'help'
        self.no_matching_args_operation = 'print'

        self.help_message = ""


    def handle_args(self, args):
        """
        Identify and execute the handler for the chosen operation

        Args:
            args (list[str]):

        """
        # Provide implicit help option
        self.operations['help'] = (
            self.operations.get('help')
            or {'handler': self.print_help}
        )

        # Index operations to include aliases
        _operations = {}
        for name, op in self.operations.items():
            for op_name in [name] + op.get('aliases', []):
                _operations[op_name] = {
                    'name': name,
                    'handler': op['handler']
                }
        log.debug(f"Operation aliases:")
        for alias, operation in _operations.items():
            log.debug(f"    {alias}: {operation['name']}")

        # If there are no arguments, use no_args_operation
        if not args:
            log.debug("No further arguments")
            log.debug(f"Defaulting to {self.no_args_operation}")
            args = [self.no_args_operation]

        # Context-specific checks on arg progression
        args, op_name, handler = self.extra_arg_checks(args)

        if not op_name:
            # If first arg matches no op_names or aliases,
            # use no_matching_args_operation
            if args[0] not in _operations:
                log.debug(f"Next arg exists but is not a valid operaion: {args[0]}")
                log.debug(f"Defaulting to {self.no_matching_args_operation}")
                args.insert(0, self.no_matching_args_operation)

            # Remove operation from args and identify handler
            operation = _operations[args.pop(0)]
            op_name, handler = operation['name'], operation['handler']

        log.debug(f"Running {str(self.__class__)} -> {op_name} with args: {args})")

        # Run lambda handlers to initialize the object
        # and get the .handle_args() method 
        if handler.__name__ == "<lambda>":
            handler = handler()

        # Run handler, passing on the remaining args
        handler(args)

    def extra_arg_checks(self, args):
        """
        App-specific CLI arg checks

        Args:
            args (list):
        Returns:
            list[str]: Updated args list
            str: Name of resulting operation
            method: Method referenced as the operation's handler

        """
        return args, None, None


    def print_help(self, args):
        """
        Print a predefined or generated help message
        for the operation

        """
        # Custom help message
        if self.help_message:
            print(self.help_message)
            return

        # Default help message is constructed from self.operations
        print(f"{str(self.__class__)} Operations:\n")
        for name, operation in self.operations.items():
            print(f"{name}:  {operation.get('help', '#TODO')}")
            if 'aliases' in operation:
                print(f"    Aliases: {operation['aliases']}")
