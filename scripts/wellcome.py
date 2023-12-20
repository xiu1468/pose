import sys
import subprocess
from PyQt5.QtWidgets import QApplication
from Ui_wellcome import Ui_Form
from PyQt5 import QtWidgets


class MyApp(Ui_Form):
    def __init__(self, dialog):
        Ui_Form.__init__(self)
        self.setupUi(dialog)
        self.pushButton.setText("啟動定位")
        self.pushButton_2.setText("語音導航與動力輔助")
        self.label.setText("歡迎使用~")
        # Add click event to the buttons
        self.pushButton.clicked.connect(self.launch)
        self.pushButton_2.clicked.connect(self.run)

    def launch(self):
        # Use subprocess to run roslaunch command
        subprocess.Popen(["roslaunch", "simple_localization", "localization.launch"])

    def run(self):
        # Use subprocess to run rosrun command
        subprocess.Popen(["rosrun", "pose", "point_tf_broadcaster.py"])
        subprocess.Popen(["python3", "testspeechguideNew.py"])
        subprocess.Popen(["python3", "motor_control.py"])
if __name__ == '__main__':
    app = QApplication(sys.argv)

    dialog = QtWidgets.QDialog()
    prog = MyApp(dialog)

    dialog.show()
    sys.exit(app.exec_())
