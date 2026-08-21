"""
Background execution.

SimulationWorker runs the built command in a QThread so the GUI stays
responsive, streaming output back to the View via Qt signals.
"""

import shlex
import subprocess

from PyQt6.QtCore import QThread, pyqtSignal


class SimulationWorker(QThread):
    """Runs the simulation executable in a background thread."""

    output_ready = pyqtSignal(str)     # streamed stdout/stderr lines
    finished_ok = pyqtSignal(int)      # emitted with the process return code
    failed = pyqtSignal(str)           # emitted with an error message

    def __init__(self, command: list, working_dir: str):
        super().__init__()
        self.command = command
        self.working_dir = working_dir
        self._process = None

    def run(self):
        try:
            self.output_ready.emit("$ " + " ".join(shlex.quote(c) for c in self.command))

            self._process = subprocess.Popen(
                self.command,
                cwd=self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            for line in self._process.stdout:
                self.output_ready.emit(line.rstrip("\n"))

            return_code = self._process.wait()
            self.finished_ok.emit(return_code)

        except FileNotFoundError:
            self.failed.emit("The executable could not be launched (file not found or not runnable).")
        except PermissionError:
            self.failed.emit("Permission denied while trying to run the executable.")
        except Exception as exc:  # pragma: no cover - safety net for unexpected errors
            self.failed.emit(f"Unexpected error while running the simulation:\n{exc}")

    def stop(self):
        """Allow the controller to terminate a running process if needed."""
        if self._process and self._process.poll() is None:
            self._process.terminate()
