from PyQt6.QtGui import QIntValidator, QFont
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
    QPlainTextEdit,
    QSizePolicy,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenModelica Model Runner")
        self.setMinimumWidth(560)
        self._build_ui()

    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setSpacing(14)
        root_layout.setContentsMargins(18, 18, 18, 18)

        root_layout.addWidget(self._build_header())

        input_group = self._build_input_group()
        root_layout.addWidget(input_group)

        root_layout.addLayout(self._build_run_row())

        output_group = self._build_output_group()
        root_layout.addWidget(output_group, stretch=1)

    def _build_header(self) -> QWidget:
        header = QWidget()
        layout = QVBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("OpenModelica Model Runner")
        title_font = QFont()
        title_font.setPointSize(15)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        subtitle = QLabel(
            "Select a compiled OpenModelica executable, set the start/stop "
            "time, then run it."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #555;")
        layout.addWidget(subtitle)

        return header

    def _build_input_group(self) -> QGroupBox:
        input_group = QGroupBox("Simulation Settings")
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        exe_row = QHBoxLayout()
        self.executable_edit = QLineEdit()
        self.executable_edit.setPlaceholderText("Path to OpenModelica executable...")
        self.browse_button = QPushButton("Browse...")
        exe_row.addWidget(self.executable_edit)
        exe_row.addWidget(self.browse_button)
        exe_row_widget = QWidget()
        exe_row_widget.setLayout(exe_row)
        form_layout.addRow("Executable:", exe_row_widget)

        self.start_time_edit = QLineEdit()
        self.start_time_edit.setPlaceholderText("e.g. 0")
        self.start_time_edit.setValidator(QIntValidator(-2_147_483_648, 2_147_483_647))
        form_layout.addRow("Start time:", self.start_time_edit)

        self.stop_time_edit = QLineEdit()
        self.stop_time_edit.setPlaceholderText("e.g. 10")
        self.stop_time_edit.setValidator(QIntValidator(-2_147_483_648, 2_147_483_647))
        form_layout.addRow("Stop time:", self.stop_time_edit)

        input_group.setLayout(form_layout)
        return input_group

    def _build_run_row(self) -> QHBoxLayout:
        run_row = QHBoxLayout()
        self.run_button = QPushButton("Run Simulation")
        self.run_button.setMinimumHeight(36)
        self.run_button.setStyleSheet("QPushButton { font-weight: bold; }")

        self.status_label = QLabel("Ready.")
        self.status_label.setStyleSheet("color: #555;")

        run_row.addWidget(self.run_button)
        run_row.addWidget(self.status_label, stretch=1)
        return run_row

    def _build_output_group(self) -> QGroupBox:
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout()

        self.output_console = QPlainTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setPlaceholderText("Simulation output will appear here...")
        self.output_console.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.output_console.setMinimumHeight(220)
        self.output_console.setStyleSheet(
            "QPlainTextEdit { font-family: Consolas, 'Courier New', monospace; "
            "background-color: #1e1e1e; color: #d4d4d4; }"
        )

        output_layout.addWidget(self.output_console)
        output_group.setLayout(output_layout)
        return output_group

    def set_running_state(self, running: bool):
        self.run_button.setEnabled(not running)
        self.browse_button.setEnabled(not running)
        self.executable_edit.setEnabled(not running)
        self.start_time_edit.setEnabled(not running)
        self.stop_time_edit.setEnabled(not running)
        self.run_button.setText("Running..." if running else "Run Simulation")

    def set_status(self, text: str, is_error: bool = False):
        color = "#c0392b" if is_error else "#27ae60"
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        self.status_label.setText(text)

    def append_output(self, text: str):
        self.output_console.appendPlainText(text)

    def clear_output(self):
        self.output_console.clear()
