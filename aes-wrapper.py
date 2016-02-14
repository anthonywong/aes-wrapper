#!/usr/bin/env python3

# Copyright (c) 2016 Anthony Wong <yp@anthonywong.net>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

import sys
import subprocess
import tempfile
import os.path
import time
import shutil
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Dialog(QDialog):
    def __init__(self, filename, encrypt=False, parent=None):
        print(filename)
        super(Dialog, self).__init__(parent)
        self.filename = filename
        self.encrypt = encrypt
        self.layout = QVBoxLayout()

        self.text = QLabel("Please input the password to " + ("encrypt" if encrypt else "decrypt") + " <i>" + filename + "</i>:")
        self.layout.addWidget(self.text)

        self.grid = QGridLayout()
        self.grid.addWidget(QLabel("Password: "), 1, 1)
        self.field = QLineEdit()
        self.field.setEchoMode(QLineEdit.Password)
        self.grid.addWidget(self.field, 1, 2)
        self.layout.addLayout(self.grid)

        self.layout2 = QHBoxLayout()
        self.b1 = QPushButton("OK")
        self.b2 = QPushButton("Cancel")
        self.b1.setCheckable(True)
        self.b1.clicked.connect(self.process)
        self.b2.clicked.connect(self.close)
        self.layout2.addStretch()
        self.layout2.addWidget(self.b1)
        self.layout2.addWidget(self.b2)
        self.layout.addLayout(self.layout2)

        self.setLayout(self.layout)
        self.setWindowTitle("Descrypt AES file")

        # Wrong password label, not shown by default
        self.error_label = QLabel("<font color='#FF0000'>Wrong password</font>")

    def process(self):
        tmp_filename = next(tempfile._get_candidate_names())
        tmp_dir = tempfile._get_default_tempdir()
        result_file = os.path.join(tmp_dir, tmp_filename)
        if not os.path.exists(result_file ):
            password = self.field.text()
            try:
                cmd = ['/usr/local/bin/aescrypt', '-e' if self.encrypt else '-d', '-p', password, '-o', result_file, self.filename]
                p = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
                self.close()
                if self.encrypt:
                    dest_file = os.path.join(os.path.dirname(self.filename), self.filename + ".aes")
                    if os.path.exists(dest_file):
                        msgBox = QMessageBox()
                        msgBox.setText("File " + dest_file + " already exists")
                        msgBox.setInformativeText("Overwrite?")
                        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        ret = msgBox.exec_();
                        if ret == QMessageBox.No:
                            return
                    shutil.move(result_file, dest_file)
                    msgBox = QMessageBox()
                    msgBox.setText("Encryption successful")
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    ret = msgBox.exec_();
                else:
                    cmd = ['xdg-open', result_file]
                    p = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                self.error_label = QLabel("<font color='#FF0000'>" + e.output.decode("utf-8") + "</font>")
                self.grid.addWidget(self.error_label, 2, 2)
                #print(e.cmd)
                #print(e.returncode)
                #print(e.output)

                # Shake the window
                i = 6
                dir = 1
                while i > 0:
                    self.move(self.x()+dir*10, self.y())
                    self.repaint()
                    dir = -dir
                    i = i - 1
                    time.sleep(0.04)

def main(argv):
    if len(argv) == 1:
        print("Usage: " + argv[0] + " <file>")
        sys.exit(1)

    app = QApplication(argv)
    if argv[1].endswith(".aes"):
        win = Dialog(argv[1], False)
    else:
        win = Dialog(argv[1], True)
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)
