Created by Alexander Yazdani
July 2024

This file acts as a standalone console application for both Windows and Mac OS.
Additionally, the ConsoleWidget class can be imported into larger PyQT6 projects as an embedded console.

The purpose of this file is to allow a developer to embed a console into a Python application, removing the need for a separate console window and creating a sleek design.
When creating an executable, the --noconsole option can be used without loss of functionality.

Features include:
 - Colored error messagiong
 - OS detection
 - Command history
 - Prints all console output from any print() lines within a python script that implements this widget
 - Allows for user input commands
