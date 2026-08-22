import os
from dataclasses import dataclass


@dataclass
class ModelConfig:
    executable_path: str
    start_time: int
    stop_time: int

    def validate(self) -> None:
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
        return [
            self.executable_path,
            f"-startTime={self.start_time}",
            f"-stopTime={self.stop_time}",
        ]


class SimulationRunner:
    def __init__(self, config: ModelConfig):
        self.config = config

    def build_command(self) -> list:
        self.config.validate()
        return self.config.to_command()
