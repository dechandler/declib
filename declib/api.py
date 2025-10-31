"""

"""
import os
import re
import sys
import threading

from subprocess import Popen, PIPE

ANSI_ESCAPE = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')


class DeclibApi:

    def __init__(self, config):

        self.config = config
        self.log = config.log

    def run_command(self,
            cmd, cwd='',
            stdin='',
            print_stdout=True, log_stdout=True,
            print_stderr=True, log_stderr=True
        ):
        """
        Utility method for running OS commands

        Args:
            cmd (list):
            cwd (str OR os.PathLike, optional):
            stdin (str, optional):
            print_stdout (bool, optional):
            log_stdout (bool, optional):
            print_stderr (bool, optional):
            log_stderr (bool, optional):

        Returns:
            stdout (list): stdout lines from running command
            stderr (list): stderr lines from running command

        """
        cwd = cwd or os.getcwd()

        self.log.info(' '.join([
            "Running command from", cwd,
            f"with{'' if stdin else 'out'} stdin:",
            ' '.join(cmd)
        ]))

        p = Popen(cmd, cwd=cwd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        threads = []

        # Start stdout listener
        stdout = []
        threads.append(threading.Thread(
            target=self._get_stream,
            args=(p.stdout, stdout),
            kwargs={'to_screen': print_stdout, 'to_log': log_stdout}
        ))
        threads[-1].start()

        # Start stderr listener
        stderr = []
        threads.append(threading.Thread(
            target=self._get_stream,
            args=(p.stderr, stderr),
            kwargs={'to_screen': print_stderr, 'to_log': log_stderr}
        ))
        threads[-1].start()

        # Pipe text into stdin
        if stdin:
            def stdin_thread_func(stdin_pipe, stdin):
                stdin_pipe.write(stdin.encode())
                stdin_pipe.close()
            threads.append(threading.Thread(
                target=stdin_thread_func,
                args=(p.stdin, stdin),
            ))
            threads[-1].start()

        # Wait for all to complete
        for thread in threads:
            thread.join()

        return stdout, stderr

    def _get_stream(self, pipe, stream_output, to_screen=True, to_log=True):

        while pipe.readable():
            line = pipe.readline()
            if not line:
                break
            line = line.decode().rstrip()

            if to_log:
                self.log.err.debug(line)
            if to_screen and self.log.err.level > 15:
                print(line)

            stream_output.append(ANSI_ESCAPE.sub('', line))
