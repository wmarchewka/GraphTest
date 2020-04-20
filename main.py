from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PySide2 import QtWidgets, QtUiTools, QtCore
from PySide2 import QtCore
import logging
import sys
import time
import math
import numpy as np
from math import sin, pi
import pyqtgraph as pg


class Graph(object):

    def __init__(self):
        super().__init__()
        logging.basicConfig(level=logging.DEBUG)
        self.log = logging.getLogger(__name__)
        self.log.debug("Test")
        self.load_graph_screen()
        self.graphwindow.SLIDER_freq1.valueChanged.connect(self.update_frequency1)
        self.graphwindow.SLIDER_amp1.valueChanged.connect(self.update_amplitude1)
        self.graphwindow.SLIDER_freq2.valueChanged.connect(self.update_frequency2)
        self.graphwindow.SLIDER_amp2.valueChanged.connect(self.update_amplitude2)
        self.graphwindow.SLIDER_trigger.valueChanged.connect(self.update_trigger)
        self.coderate = 75
        self.pps = self.coderate / 60
        self.px_per_sec = 500
        self.freq_mult = 1
        self.hl = self.graphwindow.horizontalLayout
        self.pw1 = pg.PlotWidget(name="plot1")
        self.hl.addWidget(self.pw1)
        graph_length = 5000
        self.pw1.setXRange(0, graph_length)
        self.pw1.setYRange(-20, 20)
        self.pw1.setAntialiasing(True)
        self.graphwindow.SLIDER_freq1.setMaximum(graph_length)
        self.graphwindow.SLIDER_freq2.setMaximum(graph_length)
        self.amp1 = 1
        self.freq1 = 10
        self.amp2 = 2
        self.freq2 = 20
        self.t = 0
        self.trigger = 0
        self.start = 0
        self.end = 100000
        self.pw1.setXRange(self.start, self.end)
        self.update()

    def load_graph_screen(self):
        try:
            self.guiname = "gui/Graph.ui"
            ui_file = QFile(self.guiname)
            ui_file.open(QFile.ReadOnly)
            loader = QUiLoader()
            self.graphwindow = loader.load(ui_file)
            ui_file.close()
            self.log.debug('Loading screen ' + self.guiname)
            self.graphwindow.showNormal()
            display_monitor = 1
            monitor = QDesktopWidget().screenGeometry(display_monitor)
            qtrect = self.graphwindow.frameGeometry()
            centerPoint = monitor.center()
            qtrect.moveCenter(centerPoint)
            self.graphwindow.move(qtrect.topLeft())

        except FileNotFoundError:
            self.log.debug("Could not find {}".format(self.guiname))  # CATCHES EXIT SHUTDOWN

    def update_trigger(self, value):
        self.log.debug("TRIGGER:{}".format(value))
        self.trigger = value

    def update_frequency1(self, value):
        self.log.debug("FREQ:{}".format(value))
        self.freq1 = value
        self.graphwindow.LBL_freq0.setText("{}".format(self.freq1))

    def update_amplitude1(self, value):
        self.amp1 = value / 50
        self.log.debug("AMP:{}".format(self.amp1))
        self.graphwindow.LBL_gain0.setText("{}".format(self.amp1))

    def update_frequency2(self, value):
        self.log.debug("FREQ:{}".format(value))
        self.freq2 = value
        self.graphwindow.LBL_freq1.setText("{}".format(self.freq2))

    def update_amplitude2(self, value):
        self.amp2 = value / 50
        self.log.debug("AMP:{}".format(self.amp2))
        self.graphwindow.LBL_gain1.setText("{}".format(self.amp2))

    def update(self):
        point_val = 50000
        points1 = point_val
        points2 = point_val
        points3 = point_val
        X1 = np.arange(points1)
        X2 = np.arange(points2) + point_val
        X3 = np.arange(points3) + point_val + point_val
        Y1 = np.sin(np.arange(points1) / points1 * self.freq1 * np.pi)
        Y2 = np.sin(np.arange(points2) / points2 * self.freq2 * np.pi)
        Y3 = np.sin(np.arange(points3) / points3 * self.freq1 * np.pi)
        self.pw1.plotItem.plot(X1, Y1 * self.amp1, pen=(1, 3), clear=True)
        self.pw1.plotItem.plot(X2, Y2 * self.amp2, pen=(3, 3), clear=False)
        self.pw1.plotItem.plot(X3, Y3 * self.amp1, pen=(1, 3), clear=False)
        self.graphwindow.CHK_more.setChecked(True)
        if self.graphwindow.CHK_more.isChecked():
            QtCore.QTimer.singleShot(10, self.update)  # QUICKLY repeat


if __name__ == "__main__":
    app = QApplication(sys.argv)
    graph = Graph()
    app.exit(app.exec_())

# points2 = point_val
# points3 = point_val
# X1 = np.arange(points1)
# X2 = np.arange(points2) + point_val
# X3 = np.arange(points3) + point_val + point_val
# Y1 = np.sin(np.arange(points1) / points1 * self.freq1 * np.pi)
# Y2 = np.sin(np.arange(points2) / points2 * self.freq2 * np.pi)
# Y3 = np.sin(np.arange(points3) / points3 * self.freq1 * np.pi)
# self.pw1.plotItem.plot(X1, Y1 * self.amp1, pen=(1, 3), clear=True)
# self.pw1.plotItem.plot(X2, Y2 * self.amp2, pen=(3, 3), clear=False)
# self.pw1.plotItem.plot(X3, Y3 * self.amp1, pen=(1, 3), clear=False)
# self.pw1.setXRange(self.start, self.end)
