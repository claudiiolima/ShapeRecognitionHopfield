import sys
sys.path.append('..')
sys.path.append('../include')
sys.path.append('../ui')

from PyQt4 import QtGui
from pyqtpaint import PyQtPaint

class SampleCode(QtGui.QDialog):
    def __init__(self, *args, **kwargs):
        super(SampleCode, self).__init__(*args, **kwargs)
        layout = QtGui.QVBoxLayout()

        # create PyQtPaint widget
        self.paint = PyQtPaint(100, 100)

        # set pen attributes
        self.paint.set_pen_color(QtGui.QColor(0, 0, 0, 255))
        self.paint.set_pen_size(7)
        self.paint.set_pen_blur(0)

        layout.addWidget(self.paint)
        self.setLayout(layout)

    def closeEvent(self, event):
        self.paint.threadpool.deleteLater()
        event.accept()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    test_window = SampleCode()
    test_window.show()
    sys.exit(app.exec_())
