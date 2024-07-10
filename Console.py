'''
Created by Alexander Yazdani
July 2024

This file acts as a standalone console application for both Windows and Mac OS.
Additionally, the ConsoleWidget class can be imported into larger PyQT6 projects as an embedded console.
'''


import sys
import subprocess
import os
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPlainTextEdit, QLineEdit, QLabel
from PyQt6.QtCore import Qt

class EmittingStream:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, text):
        text = text.replace('\n', '<br>')
        self.text_edit.appendHtml(f"<span style='color: green;'>{text}</span>")
    
    def flush(self):
        pass

class ConsoleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                border: 2px solid black;
                background-color: black;
            }
            QPlainTextEdit, QLabel, QLineEdit {
                background-color: black;
                color: green;
                font-family: Consolas, monospace;
            }
            QLineEdit {
                border: none;
                box-shadow: none;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.console_output = QPlainTextEdit(self)
        self.console_output.setReadOnly(True)
        self.console_output.mousePressEvent = self.focus_input
        
        self.console_input = QLineEdit(self)
        self.console_input.returnPressed.connect(self.on_enter)
        self.console_input.keyPressEvent = self.handle_key_press
        
        self.prompt_label = QLabel()
        self.update_prompt()
        
        input_layout = QHBoxLayout()
        input_layout.setSpacing(0)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.addWidget(self.prompt_label)
        input_layout.addWidget(self.console_input)
        
        self.layout.addWidget(self.console_output)
        self.layout.addLayout(input_layout)

        self.setMouseTracking(True)
        self.mousePressEvent = self.focus_input
        
        self.command_history = []
        self.history_index = -1
        
        sys.stdout = EmittingStream(self.console_output)
        sys.stderr = EmittingStream(self.console_output)
        
    def focus_input(self, event):
        self.console_input.setFocus()

    def handle_key_press(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.show_previous_command()
        elif event.key() == Qt.Key.Key_Down:
            self.show_next_command()
        else:
            QLineEdit.keyPressEvent(self.console_input, event)
        
    def show_previous_command(self):
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.console_input.setText(self.command_history[self.history_index])
    
    def show_next_command(self):
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.console_input.setText(self.command_history[self.history_index])
        elif self.history_index == len(self.command_history) - 1:
            self.history_index += 1
            self.console_input.clear()
    
    def update_prompt(self):
        current_directory = os.getcwd()
        self.prompt_label.setText(f"{current_directory}>")
        
    def on_enter(self):
        command = self.console_input.text()
        if command:
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            current_directory = os.getcwd()
            self.console_output.appendHtml(f"<span style='color: green;'>{current_directory}> {command}</span>")
            self.console_input.clear()
            self.execute_command(command)
            self.update_prompt()
    
    def execute_command(self, command):
        if command.startswith('cd '):
            self.change_directory(command[3:].strip())
            self.console_output.appendPlainText("")
        else:
            self.run_shell_command(command)
    
    def change_directory(self, path):
        try:
            os.chdir(path)
        except Exception as e:
            self.console_output.appendHtml(f"<span style='color: orange;'>Error: {str(e)}</span>")

    def run_shell_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.stdout:
                self.console_output.appendPlainText(result.stdout)
            if result.stderr:
                self.console_output.appendHtml(f"<span style='color: orange;'>{result.stderr}</span>")
                self.console_output.appendPlainText("")
        except Exception as e:
            self.console_output.appendHtml(f"<span style='color: red;'>Error: {str(e)}</span>")
            self.console_output.appendPlainText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    console_widget = ConsoleWidget()
    console_widget.show()
    sys.exit(app.exec())
