from PySide6 import QtCore, QtWidgets
import sys
import queue
import time
import keyboard

from config import Config
from utils.driver_manager import DriverManager
from utils.input_handler import InputHandler
from commands.command_executor import CommandExecutor


class AssistantWorker(QtCore.QThread):
    log = QtCore.Signal(str)
    finished_signal = QtCore.Signal()

    def __init__(self, mode: str):
        super().__init__()
        self.mode = mode
        self.command_queue = queue.Queue()
        self._running = False

    def run(self):
        self._running = True
        try:
            Config.set_input_mode(self.mode)
            driver_manager = DriverManager()
            input_handler = InputHandler(self.mode)
            # expose input_handler so stop() can request interruption
            self.input_handler = input_handler
            command_executor = CommandExecutor(driver_manager, input_handler)

            first_voice_command = True

            while self._running:
                # Check for manual commands first
                try:
                    cmd = self.command_queue.get_nowait()
                except queue.Empty:
                    cmd = None

                if cmd:
                    self.log.emit(f"Manual: {cmd}")
                    cont = True
                    try:
                        cont = command_executor.execute(cmd)
                    except Exception as e:
                        self.log.emit(f"Error executing command: {e}")
                    if not cont:
                        break
                    continue

                # Voice mode handling
                if self.mode.startswith("voice"):
                    try:
                        command = input_handler.get_command(first_run=first_voice_command)
                    except Exception as e:
                        self.log.emit(f"Input handler error: {e}")
                        break

                    first_voice_command = False
                    if command is None:
                        break
                    self.log.emit(f"Voice: {command}")
                    try:
                        cont = command_executor.execute(command)
                    except Exception as e:
                        self.log.emit(f"Error executing command: {e}")
                        cont = True
                    if not cont:
                        break
                else:
                    # Typing mode: idle waiting for commands
                    time.sleep(0.15)

        finally:
            try:
                driver_manager.cleanup()
            except Exception:
                pass
            self.finished_signal.emit()

    def stop(self):
        self._running = False
        # request stop on input handler's voice input to interrupt blocking listens
        try:
            if hasattr(self, 'input_handler') and getattr(self.input_handler, 'voice_input', None):
                try:
                    self.input_handler.voice_input.request_stop()
                except Exception:
                    pass
        except Exception:
            pass


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.Signal(str)

    def write(self, text):
        if text:
            # Emit text so UI can append it
            self.textWritten.emit(str(text))

    def flush(self):
        pass


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, emitter: EmittingStream = None):
        super().__init__()
        self.setWindowTitle("JJ Voice Assistant - GUI")

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        layout = QtWidgets.QVBoxLayout(central)

        # Controls
        hl = QtWidgets.QHBoxLayout()
        self.mode_select = QtWidgets.QComboBox()
        self.mode_select.addItems(["voice_continuous", "voice_button", "typing"])
        hl.addWidget(self.mode_select)
        # Update typing widgets when mode changes
        self.mode_select.currentTextChanged.connect(self.update_typing_widgets)

        self.start_btn = QtWidgets.QPushButton("Start")
        self.start_btn.clicked.connect(self.start_assistant)
        hl.addWidget(self.start_btn)

        self.stop_btn = QtWidgets.QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_assistant)
        self.stop_btn.setEnabled(False)
        hl.addWidget(self.stop_btn)

        layout.addLayout(hl)

        # Log area
        self.log_view = QtWidgets.QTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(self.log_view)

        # Manual command entry
        cmd_h = QtWidgets.QHBoxLayout()
        self.cmd_input = QtWidgets.QLineEdit()
        self.cmd_input.setPlaceholderText("Type a command (e.g. play Despacito in spotify)")
        cmd_h.addWidget(self.cmd_input)
        self.send_btn = QtWidgets.QPushButton("Send")
        self.send_btn.clicked.connect(self.send_command)
        cmd_h.addWidget(self.send_btn)
        layout.addLayout(cmd_h)

        # Initialize typing widget state
        self.update_typing_widgets()

        # Enter key behavior: in typing mode, pressing Enter sends the command
        self.cmd_input.returnPressed.connect(self.on_return_pressed)

        self.worker = None

    def append_log(self, text: str):
        self.log_view.append(text)

    def start_assistant(self):
        if self.worker is not None and self.worker.isRunning():
            self.append_log("Assistant already running")
            return

        mode = self.mode_select.currentText()
        self.worker = AssistantWorker(mode)
        self.worker.log.connect(self.append_log)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()

        # While running, prevent changing input mode
        self.mode_select.setEnabled(False)
        # Ensure typing widgets reflect active mode while running
        self.update_typing_widgets()

        self.append_log(f"Started assistant in mode: {mode}")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop_assistant(self):
        if not self.worker:
            return
        self.append_log("Stopping assistant...")
        # Signal worker to stop and send ESC to interrupt any blocking voice listen
        try:
            self.worker.stop()
            # emulate ESC press to interrupt voice loops in VoiceInput
            keyboard.press_and_release('esc')
        except Exception:
            pass
        self.stop_btn.setEnabled(False)

    def on_finished(self):
        self.append_log("Assistant stopped")
        # Re-enable mode selector once fully stopped
        self.mode_select.setEnabled(True)
        # Restore typing widget state based on selected mode
        self.update_typing_widgets()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.worker = None

    def update_typing_widgets(self):
        # Enable the typing input and send button only when typing mode selected
        is_typing = self.mode_select.currentText() == "typing"
        self.cmd_input.setEnabled(is_typing)
        self.send_btn.setEnabled(is_typing)

    def send_command(self):
        txt = self.cmd_input.text().strip()
        if not txt:
            return
        if self.worker and self.worker.isRunning():
            self.worker.command_queue.put(txt)
            self.append_log(f"Queued: {txt}")
            self.cmd_input.clear()
        else:
            self.append_log("Start the assistant first to send commands")

    def on_return_pressed(self):
        # Only send on Enter when typing mode is active
        if self.mode_select.currentText() == "typing":
            self.send_command()
        else:
            # In non-typing modes, do nothing on Enter (user can still click Send)
            pass


def main():
    Config.load_config()
    app = QtWidgets.QApplication(sys.argv)

    # Redirect stdout/stderr to the GUI log
    stdout_orig = sys.stdout
    stderr_orig = sys.stderr
    emitter = EmittingStream()

    sys.stdout = emitter
    sys.stderr = emitter

    w = MainWindow(emitter=emitter)
    # connect emitter to window log
    emitter.textWritten.connect(w.append_log)

    w.resize(700, 500)
    w.show()
    try:
        exit_code = app.exec()
    finally:
        # restore original streams
        sys.stdout = stdout_orig
        sys.stderr = stderr_orig

    sys.exit(exit_code)

if __name__ == "__main__":
    main()