# -*- coding: utf-8 -*-
import cv2
import os
import sys
import time
from threading import Thread

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, \
     QLabel, QGraphicsScene, QApplication
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import QTimer, Qt, pyqtSignal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(BASE_DIR)
sys.path.append(ROOT_DIR)

from python.InfraredTracker import Ui_MainWindow
from python.tracking import get_tracker


class IFTracker(QMainWindow, Ui_MainWindow):
    # define a signal
    # init_finished = pyqtSignal()
    def __init__(self, gpu_id=0):
        """
        :param gpu_id:
        """
        super(IFTracker, self).__init__()
        self.setupUi(self)

        self.__src_path = ""
        self.__cur_fidx = 0
        # self.__file_type = "image"  # image or video
        self.__total_files = 0
        self.__files = list()
        self.__is_start = False
        self.__cur_img = None
        self.__image_type = ['jpg', 'png', 'bmp']
        self.__video_type = ['mp4', 'avi']

        self.comboBox.addItems([
            'TrackerKCF',
            'TrackerMIL',
            'TrackerTLD',
            'TrackerCSRT',
            'TrackerMOSSE',
            'TrackerGOTURN',
            'TrackerBoosting',
            'TrackerMedianFlow',
        ])
        self.comboBox.setCurrentIndex(0)

        self.init_tracker = False
        self.roi_rect = None
        self.tracker = None
        self.init_single_slot_connect()

        self.timer = QTimer()
        self.timer.setInterval(30)
        self.timer.timeout.connect(self.main_working)    # work thread

    def init_single_slot_connect(self):
        self.pushButtonLoadVideo.clicked.connect(self.load_video)
        self.pushButtonPlay.clicked.connect(self.start_working)
        self.horizontalSlider.valueChanged[int].connect(self.change_value)
        self.comboBox.currentIndexChanged[int].connect(self.currentIndexChanged)
        self.checkBox.stateChanged[int].connect(self.graphicsView.setEnableDrawRects)
        self.graphicsView.mouse_release_up.connect(self.get_roi_rect)

    def get_roi_rect(self):
        spt, ept = self.graphicsView.getRect()
        self.roi_rect = (round(spt.x()), round(spt.y()), round(ept.x() - spt.x()), round(ept.y() - spt.y()))

    def show_image(self, image):
        qimg = self.cvimg_to_qimg(image)
        self.graphicsView.setPixmap(QPixmap.fromImage(qimg))
        
        self.horizontalSlider.setValue(self.__cur_fidx + 1)
        self.labelSlider.setText("{}/{}".format(self.__cur_fidx + 1, self.__total_files))

    def load_video(self):
        tmp_path = self.__src_path
        tmp_path = QFileDialog.getExistingDirectory(self, "Load", tmp_path)
        # tmp_path = QFileDialog.getOpenFileName(self, 'Open Files', tmp_path)
        if not os.path.exists(tmp_path):
            return

        self.__src_path = tmp_path

        # 可採用迭代器優化
        self.__files = sorted([f for f in os.listdir(self.__src_path)
                              if f.split('.')[-1] in self.__image_type])

        self.__total_files = len(self.__files)
        if self.__total_files == 0:
            QMessageBox.warning(self, "Information", "The selected directory is empty!")
            return

        self.init_tracker = False
        self.__cur_fidx = 0
        self.horizontalSlider.setRange(1, self.__total_files)
        self.horizontalSlider.setValue(1)

        # self.labelSlider.setText('{}/{}'.format(self.__cur_fidx + 1, self.__total_files))
        # pre-read an image for display
        self.__cur_img = cv2.imread(os.path.join(self.__src_path, self.__files[self.__cur_fidx]))
        self.show_image(self.__cur_img.copy())

    def change_value(self, cur_idx):
        self.__cur_fidx = cur_idx - 1
        self.labelSlider.setText('{}/{}'.format(cur_idx, self.__total_files))
        # if not self.__is_start:
        #     self.__cur_img = cv2.imread(os.path.join(self.__src_path, self.__files[cur_idx]), -1)
        #     self.show_image(self.__cur_img.copy())

    def currentIndexChanged(self, index):
        if self.tracker is not None and self.tracker.isWorking():
            self.tracker.stopTracking()
            self.init_tracker = False

    @staticmethod
    def cvimg_to_qimg(image):
        shape = image.shape
        if image.ndim == 4:
            res_img = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
            res_img = QImage(res_img.data, shape[1], shape[0], shape[1] * 4, QImage.Format_ARGB32)
        elif image.ndim == 3:
            res_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            res_img = QImage(res_img.data, shape[1], shape[0], shape[1] * 3, QImage.Format_RGB888)
        elif image.ndim == 2:
            res_img = QImage(image.data, shape[1], shape[0], shape[1] * 1, QImage.Format_Grayscale8)
        else:
            raise Exception("image channels must be 1, 3 or 4")

        return res_img

    def main_working(self):
        img_temp = None
        self.__cur_img = cv2.imread(os.path.join(self.__src_path, self.__files[self.__cur_fidx]))
        if self.checkBox.isChecked():
            # tracking
            if not self.init_tracker:
                self.tracker = get_tracker(self.comboBox.currentText())()
                self.tracker.initTracker(self.__cur_img.copy(), self.roi_rect)
                self.init_tracker = True
            else:
                self.tracker.tracking(self.__cur_img.copy())
            
            bbox = self.tracker.getResults()
            img_temp = self.__cur_img.copy()
            cv2.rectangle(img_temp, (int(bbox[0]), int(bbox[1])), (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])), (0, 0, 255), 1)
        else:
            img_temp = self.__cur_img.copy()
        
        self.show_image(img_temp)

        self.__cur_fidx += 1
        if self.__cur_fidx >= self.__total_files:
            # no more files, stop timer
            self.pushButtonPlay.clicked.emit()
            return

    def start_working(self):
        self.graphicsView.clearRects()

        if self.__total_files == 0:
            QMessageBox.warning(self, u"Information", u"Please select a directory")
            return
        if self.__is_start:
            # stop working
            self.pushButtonPlay.setText(u'开始')
            self.timer.stop()
            self.__is_start = False
        elif self.__cur_fidx < self.__total_files:
            # start working
            self.pushButtonPlay.setText(u'停止')
            self.timer.start()
            self.__is_start = True
        else:
            QMessageBox.warning(self, u"Warning", u"Detecting finish!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    iftracker = IFTracker()
    iftracker.show()
    sys.exit(app.exec_())
