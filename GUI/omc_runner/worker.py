import shlex
import subprocess

from PyQt6.QtCore import QThread, pyqtSignal


class SimulationWorker(QThread):
    output_ready = pyqtSignal(str)     
    finished_ok = pyqtSignal(int)      
    failed = pyqtSignal(str)           

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
        except Exception as exc:  
            self.failed.emit(f"Unexpected error while running the simulation:\n{exc}")

    def stop(self):
        if self._process and self._process.poll() is None:
            self._process.terminate()
