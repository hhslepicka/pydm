import os
from PyQt5.QtDesigner import QFormBuilder
from PyQt5.QtWidgets import QLabel, QWidget, QApplication
from PyQt5.QtCore import QFile

app = QApplication([])
display = QWidget()
display.setObjectName("MyDisplay")
display.setWindowTitle("Test Display")

frame = QFrame(parent=display)
frame.setObjectName("frm1")

label = QLabel(parent=frame)        
label.setParent(frame)
label.setObjectName("btn_"+str(1))
label.setText("Test Label")

fb = QFormBuilder()
designer_path = os.getenv("PYQTDESIGNERPATH", "")
for entry in designer_path.split(os.pathsep):
    if entry != "":
        fb.addPluginPath(entry)
_file = QFile("test_save.ui")
_file.open(QFile.ReadWrite)

fb.save(_file, display)
_file.close()
