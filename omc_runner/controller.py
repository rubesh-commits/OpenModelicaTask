"""
Controller layer.

AppController is the only class that knows about both the View and the
Model/worker. It connects View signals (button clicks) to Model actions
and feeds results (output, status, errors) back into the View.
"""

import os

from PyQt6.QtWidgets import QFileDialog, QMessageBox

from .model import ModelConfig, SimulationRunner
from .view import MainWindow
from .worker import SimulationWorker


class AppController:
    """Connects the View's signals to Model actions."""

    def __init__(self, view: MainWindow):
        self.view = view
        self.worker: SimulationWorker | None = None

        self.view.browse_button.clicked.connect(self.on_browse_clicked)
        self.view.run_button.clicked.connect(self.on_run_clicked)

    # --- Event handlers -------------------------------------------------

    def on_browse_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Select OpenModelica Executable",
            "",
            "All Files (*)" if os.name != "nt" else "Executable Files (*.exe);;All Files (*)",
        )
        if path:
            self.view.executable_edit.setText(path)

    def on_run_clicked(self):
        self.view.clear_output()
        self.view.set_status("Validating inputs...")

        config = self._read_config_from_view()
        if config is None:
            return

        runner = SimulationRunner(config)
        try:
            command = runner.build_command()
        except ValueError as exc:
            self._show_error(str(exc))
            return

        self._start_worker(command, working_dir=os.path.dirname(config.executable_path) or ".")

    def on_finished(self, return_code: int):
        self.view.set_running_state(False)
        if return_code == 0:
            self.view.set_status("Simulation finished successfully.")
        else:
            self.view.set_status(f"Simulation exited with code {return_code}.", is_error=True)

    def on_failed(self, message: str):
        self.view.set_running_state(False)
        self.view.set_status("Simulation failed.", is_error=True)
        self.view.append_output(f"[ERROR] {message}")
        self._show_error(message)

    # --- Helpers ----------------------------------------------------------

    def _read_config_from_view(self) -> ModelConfig | None:
        """Read and type-check the raw form input; show a dialog on failure."""
        exe_path = self.view.executable_edit.text().strip()
        start_text = self.view.start_time_edit.text().strip()
        stop_text = self.view.stop_time_edit.text().strip()

        if not start_text or not stop_text:
            self._show_error("Please enter both a start time and a stop time.")
            return None

        try:
            start_time = int(start_text)
            stop_time = int(stop_text)
        except ValueError:
            self._show_error("Start time and stop time must be whole numbers.")
            return None

        return ModelConfig(
            executable_path=exe_path,
            start_time=start_time,
            stop_time=stop_time,
        )

    def _start_worker(self, command: list, working_dir: str):
        self.view.set_status("Running simulation...")
        self.view.set_running_state(True)

        self.worker = SimulationWorker(command, working_dir)
        self.worker.output_ready.connect(self.view.append_output)
        self.worker.finished_ok.connect(self.on_finished)
        self.worker.failed.connect(self.on_failed)
        self.worker.start()

    def _show_error(self, message: str):
        self.view.set_status("Error - see dialog.", is_error=True)
        QMessageBox.critical(self.view, "Error", message)
