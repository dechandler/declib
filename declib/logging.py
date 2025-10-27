"""


"""
import logging
import os
import sys


class DeclibLogger:

    def __init__(self):

        self._pre_log_messages = []
        self.log = self._pre_log


    def _pre_log(self, log_level, message):
        """
        Since things can be logged before logs are configured,
            add timestamp and stash log messages for later replay
            into the correct log

        Args:
            log_level (str or int): Accepts named log levels
                or numeric values

        """
        # self.err.log(log_level, message)
        message = f"{datetime.datetime.now().strftime("%H:%M:%S")} {message}"
        self._pre_log_messages.append((log_level, message))

    def _write_logs(self, log_level, message):
        """
        Replaces ._pre_log() as .log() backend once logging
            is configured

        Sends the message to the file logger and the stderr logger

        Args:
            log_level (str or int): Accepts named log levels
                or numeric values
            message (str): Message to publish for loggers

        """
        log_level = self._log_level_value(log_level)
        self._log.log(log_level, message)
        self.err.log(log_level, message)


    # Convenience passthrough methods to shorten log calls,
    #   eg, `self.log.log.debug()` to `self.log.debug()`
    def debug(self, message): # 10
        self.log('debug', message)
    def info(self, message): # 20
        self.log('info', message)
    def warn(self, message): # 30
        self.log('warn', message)
    def warning(self, message):  # 30
        self.log('warning', message)
    def error(self, message):  # 40
        self.log('error', message)
    def critical(self, message):  # 50
        self.log('critical', message)
    def fatal(self, message):  # 50
        self.log('fatal', message)


    def configure_loggers(self, config):
        """
        Configure file and stderr loggers, then flush the
            contents of pre-log to the loggers

        Args:
            config (dict): Configuration object or dict containing values for
                'stderr_log_level', 'log_level' and 'log_path'

        """
        # Configure stderr and file loggers
        self.err = self._configure_stderr(
            config.name, config['stderr_log_level']
        )
        self._log = self._configure_log(
            config.name,
            config['log_level'],
            config['log_path']
        )

        # Set logging for configured handlers and flush pre-log
        self.log = self._write_logs
        self._flush_pre_log()


    def _log_level_value(self, log_level):
        """
        Convenience method for normalizing log level values
            to the numerical value used internally by logging

        Args:
            log_level (str or int): Log level value to be numericized

        Returns:
            int: Numeric value of the input log level

        """
        if type(log_level) is str: 
            log_level = getattr(logging, log_level.upper())
        return log_level


    def _configure_stderr(self, name, log_level):
        """
        Configure the handler for stderr log output, and return
            the Logger

        Args:
            name (str): App name
            log_level (str or int): Log level, in either
                named or numeric form
        Returns:
            logging.Logger: Logger configured for stderr output

        """
        log_level = self._log_level_value(log_level)

        # Setup logger for stderr output
        stderr = logging.getLogger(f"{name}-stderr")
        stderr.setLevel(log_level)

        # Configure stderr log handler
        handler = logging.StreamHandler(stream=sys.stderr)
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        stderr.addHandler(handler)

        return stderr

    def _configure_log(self, name, log_level, log_path):
        """
        Configure the handler for stderr log output, and return
            the Logger

        Args:
            name (str): App name
            log_level (str or int): Log level, in either
                named or numeric form
            log_path (str or os.PathLike): Path of app log file
        Returns:
            logging.Logger: Logger configured for stderr output

        """
        log_level = self._log_level_value(log_level)

        # Setup app file log
        log = logging.getLogger(name)
        log.setLevel(log_level)

        # Ensure log file's directory
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        # Set log file handler
        handler = logging.FileHandler(log_path)
        msgfmt = "%(asctime)s (%(process)d) %(levelname)-7s: %(message)s"
        datefmt = "%Y-%m-%d_%H:%M:%S"
        handler.setFormatter(logging.Formatter(msgfmt, datefmt=datefmt))
        log.addHandler(handler)

        return log


    def _flush_pre_log(self):
        """
        Flush self._pre_log_messages into the updated log method

        """
        for level, message in self._pre_log_messages:
            self.log(level, message)
        self._pre_log_messages = []
