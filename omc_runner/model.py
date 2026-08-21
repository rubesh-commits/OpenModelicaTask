"""
Model layer.

Holds the run configuration (ModelConfig) and the logic that turns a
validated configuration into an executable command (SimulationRunner).
No Qt / GUI imports belong in this file - it should be usable and
testable completely on its own.
"""

import os
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """Holds the configuration for a single simulation run."""
    executable_path: str
    start_time: int
    stop_time: int

    def validate(self) -> None:
        """Raise ValueError with a clear message if the config is invalid."""
        if not self.executable_path:
            raise ValueError("No executable selected. Please choose an executable first.")

        if not os.path.isfile(self.executable_path):
            raise ValueError(f"Executable not found:\n{self.executable_path}")

        if os.name != "nt" and not os.access(self.executable_path, os.X_OK):
            raise ValueError(
                "The selected file is not executable.\n"
                "On Linux/macOS, run: chmod +x \"{}\"".format(self.executable_path)
            )

        if self.start_time >= self.stop_time:
            raise ValueError("Start time must be strictly less than stop time.")

    def to_command(self) -> list:
        """
        Build the command list to execute.

        OMC-generated simulation executables have dedicated runtime flags
        for the simulation window:
            ./Model -override=startTime=<start> -stopTime=<stop>
        `-override` only overrides *model parameters/variables* found in
        the XML setup file - startTime/stopTime are not model variables,
        so passing them via -override silently does nothing (and prints a
        "variable name not found in model" warning). The dedicated
        `-startTime=<value>` and `-stopTime=<value>` flags are the correct
        way to set the simulation window, so those are used here.
        """
        return [
            self.executable_path,
            f"-startTime={self.start_time}",
            f"-stopTime={self.stop_time}",
        ]


class SimulationRunner:
    """
    Turns a ModelConfig into a runnable subprocess command. Kept separate
    from any Qt/threading concerns so it can be tested or reused
    independently of the GUI.
    """

    def __init__(self, config: ModelConfig):
        self.config = config

    def build_command(self) -> list:
        self.config.validate()
        return self.config.to_command()
