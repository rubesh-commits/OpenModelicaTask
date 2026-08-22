# OpenModelica Model Runner

A simple PyQt6 desktop app to run a compiled OpenModelica simulation
executable with a chosen **start time** and **stop time**.

---

## 1. What it does

1. You pick a compiled OpenModelica executable (the file produced when you
   build a `.mo` model, e.g. `Model.exe` on Windows or `./Model` on
   Linux/macOS).
2. You enter an integer **start time** and **stop time**.
3. Click **Run Simulation** — the app runs the executable in the background
   (the GUI stays responsive) as:

   ```
   <your_executable> -override startTime=<start>,stopTime=<stop>
   ```

   This `-override startTime=...,stopTime=...` flag is the standard way
   OpenModelica-generated executables accept simulation start/stop times.
4. Live output (stdout/stderr) streams into the console panel, and the
   status label tells you when the run succeeds or fails.

---

## 2. Requirements

- Python 3.9+
- PyQt6

Install the dependency:

```bash
pip install PyQt6
```

(Optional but recommended) use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install PyQt6
```

---

## 3. Running the app

From the folder containing `main.py`:

```bash
python main.py
```

The GUI window will open.

---

## 4. Using the app

1. **Executable** — click **Browse...** and select your OpenModelica
   simulation executable.
   - On Linux/macOS, make sure the file is executable first:
     ```bash
     chmod +x /path/to/YourModel
     ```
2. **Start time** — enter a whole number (e.g. `0`).
3. **Stop time** — enter a whole number greater than the start time
   (e.g. `10`).
4. Click **Run Simulation**.
   - Inputs are validated before anything runs — you'll get a clear popup
     if the executable is missing, not executable, or the times are
     invalid.
   - While running, the inputs and button are disabled and the button
     reads "Running...".
   - Output appears live in the black console panel at the bottom.
   - When finished, the status line turns green ("Simulation finished
     successfully") or red (non-zero exit code / error), and the popup
     explains what went wrong if it failed.

---

## 5. Project structure (OOP design)

| Class               | Role                                                                 |
|---------------------|-----------------------------------------------------------------------|
| `ModelConfig`        | Data class holding executable path, start time, stop time; validates itself |
| `SimulationRunner`    | Model: turns a valid `ModelConfig` into the command to execute        |
| `SimulationWorker`    | `QThread` subclass: runs the command in the background, streams output via Qt signals |
| `MainWindow`          | View: builds/lays out all widgets only, no business logic             |
| `AppController`       | Controller: wires View events to Model actions and updates the View with results |

This keeps the GUI, the execution logic, and the coordination between them
in separate, independently testable classes.

---

## 6. Troubleshooting

- **"Executable not found"** — double-check the path in the Executable
  field, or re-browse for the file.
- **"The selected file is not executable" (Linux/macOS)** — run
  `chmod +x /path/to/YourModel` and try again.
- **"Start time must be strictly less than stop time"** — fix the two
  time fields so start < stop.
- **Nothing happens when clicking Run** — check the status label and any
  popup dialog; validation errors are always shown there.
