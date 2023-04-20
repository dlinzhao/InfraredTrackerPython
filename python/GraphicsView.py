from PyQt5.QtCore import Qt, QRect, QRectF, QPoint, pyqtSignal
from PyQt5.QtGui import QPen, QPixmap
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene

class GraphicsView(QGraphicsView):
    mouse_press_down = pyqtSignal()
    mouse_move = pyqtSignal()
    mouse_release_up = pyqtSignal()

    def __init__(self, parent: QWidget=None):
        super(GraphicsView, self).__init__(parent)

        self.start_point = QPoint(0, 0)
        self.end_point = QPoint(0, 0)

        self.flag = False
        self.is_draw_rect = False
        self.mouse_left_button_pressdown = False
        self.rect_item_ = None

        self.cur_pen_ = QPen()
        self.cur_pen_.setStyle(Qt.SolidLine)
        self.cur_pen_.setColor(Qt.blue)
        self.cur_pen_.setWidth(1)

        self.display_scene_ = QGraphicsScene()
        self.setScene(self.display_scene_)
        self.pixmap_item_ = self.display_scene_.addPixmap(QPixmap())

    def setPixmap(self, pixmap: QPixmap):
        self.pixmap_item_.setPixmap(pixmap)
        self.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.fitInView(self.pixmap_item_, Qt.KeepAspectRatio)

    def getRect(self):
        spt = self.pixmap_item_.mapFromScene(self.start_point)
        ept = self.pixmap_item_.mapFromScene(self.end_point)
        return spt, ept

    def clearRects(self):
        # for ri in self.rect_items_:
        #     self.display_scene_.removeItem(ri)
        #     del ri
        #     ri = None
        # self.rect_items_.clear()
        self.display_scene_.removeItem(self.rect_item_)
        self.rect_item_ = None

    def setEnableDrawRects(self, draw):
        self.is_draw_rect = draw > 0

    def resize(self):
        self.fitInView(self.pixmap_item_, Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        self.resize()
        return QGraphicsView.resizeEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.is_draw_rect and (event.buttons() & Qt.LeftButton):
            spts = self.mapToScene(event.pos())
            if spts.x() < 0 or spts.y() < 0 or \
                spts.x() > self.display_scene_.width() or \
                spts.y() > self.display_scene_.height():
                return
            
            if not self.flag:
                self.rect_item_ = self.display_scene_.addRect(QRectF(), self.cur_pen_)
                self.rect_item_.setZValue(1)
                self.start_point = spts
                self.flag = True
            
            self.end_point = spts
            self.rect_item_.setRect(QRectF(self.start_point, self.end_point))
            self.mouse_left_button_pressdown = True
        
        return QGraphicsView.mouseMoveEvent(self, event)
        
    def mouseReleaseEvent(self, event):
        if self.is_draw_rect and self.mouse_left_button_pressdown and (event.button() & Qt.LeftButton):
            self.mouse_left_button_pressdown = False
            self.flag = False
            # self.rect_items_.append(self.rect_item_)
            self.mouse_release_up.emit()

        return QGraphicsView.mouseReleaseEvent(self, event)
