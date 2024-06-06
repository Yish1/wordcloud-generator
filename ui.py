from PyQt5 import QtCore, QtGui, QtWidgets


class ZoomableGraphicsView(QtWidgets.QGraphicsView):  # 重载以实现鼠标拖拽、缩放功能
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.scale_factor = 1.15
        self.max_scale = 7.0  # 设置放大的上限
        self.min_scale = 0.3  # 设置缩小的上限
        self.last_pos = QtCore.QPointF()  # 记录上一次鼠标位置

    def wheelEvent(self, event):
        # 获取鼠标在视图中的位置
        old_pos = self.mapToScene(event.pos())
        # 进行缩放
        if event.angleDelta().y() > 0:  # 向上滚动
            if self.transform().m11() < self.max_scale:
                self.scale(self.scale_factor, self.scale_factor)
        else:  # 向下滚动
            if self.transform().m11() > self.min_scale:
                self.scale(1 / self.scale_factor, 1 / self.scale_factor)
        # 获取缩放后的新位置
        new_pos = self.mapToScene(event.pos())
        # 调整视图以使得鼠标位置不变
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            delta = event.pos() - self.last_pos
            self.last_pos = event.pos()
            self.horizontalScrollBar().setValue(
                int(self.horizontalScrollBar().value() - delta.x()))
            self.verticalScrollBar().setValue(int(self.verticalScrollBar().value() - delta.y()))
            #此处必须int，不然容易闪退
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.last_pos = QtCore.QPointF()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(800, 300)
        MainWindow.setMinimumSize(QtCore.QSize(700, 280))
        icon = QtGui.QIcon("wc.ico")
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        # url输入框
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit.setDragEnabled(False)
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setPlaceholderText("")
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_3.addWidget(self.lineEdit, 1, 0, 1, 1)
        # label以及滚动条
        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")
        self.label = QtWidgets.QLabel()
        self.label.setObjectName("label")
        self.label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setWordWrap(True)
        self.scroll_area.setWidget(self.label)
        self.gridLayout_3.addWidget(self.scroll_area, 3, 0, 1, 1)
        # 开始按钮
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setFixedHeight(50)
        self.gridLayout_3.addWidget(self.pushButton, 4, 0, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = ZoomableGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.hide()
        self.progressBar.setProperty("value", 0)
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        # 菜单

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def trigger_button_click(self):
        self.pushButton.click()


class select_font(QtWidgets.QDialog):  # 字体选择窗口
    def showFontDialog(self):
        self.dialog = QtWidgets.QDialog()
        self.dialog.setMinimumSize(300, 200)
        icon = QtGui.QIcon("wc.ico")
        self.dialog.setWindowIcon(icon)
        layout = QtWidgets.QVBoxLayout(self.dialog)
        self.fontComboBox = QtWidgets.QFontComboBox()
        self.preview_text = '''
            0123456789 !@#$%^&*()_+-=[]{}|;:'\",.<>/?\n\n
            沉梦小站(cmxz.top)是一个密切关注IT互联网、勤于技术分享的个人博客\n\n
            Deep Dream Blog (cmxz.top) is a personal blog focusing on the IT and internet industry, passionate about sharing technical knowledge..\n\n
            请选择适合当前语言的字体，否则词云可能无法正常显示！\n\n
            Please select a font suitable for the current language, otherwise the word cloud may not display correctly!\n\n
        '''
        self.fontPreviewLabel = QtWidgets.QLabel(self.preview_text)
        self.fontPreviewLabel.setWordWrap(True)
        layout.addWidget(self.fontComboBox)
        layout.addWidget(self.fontPreviewLabel)
        self.ok_button = QtWidgets.QPushButton("确定")
        self.ok_button.clicked.connect(self.dialog.accept)  # 关闭对话框
        layout.addWidget(self.ok_button)

    def updateFontPreview(self, font):
        self.fontPreviewLabel.setFont(font)
        self.fontPreviewLabel.setText(self.preview_text)
        self.dialog.adjustSize()  # 窗口大小自适应


class CustomDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 300)
        icon = QtGui.QIcon("wc.ico")
        self.setWindowIcon(icon)
        self.layout = QtWidgets.QVBoxLayout()
        self.cust_text = QtWidgets.QTextEdit(self)
        self.cust_text.setMinimumHeight(200)
        self.layout.addWidget(self.cust_text)
        self.setLayout(self.layout)


class Language_select(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 100)
        icon = QtGui.QIcon("wc.ico")
        self.setWindowIcon(icon)
        self.layout = QtWidgets.QVBoxLayout()
        self.comboBox = QtWidgets.QComboBox()
        self.layout.addWidget(self.comboBox)
        self.setLayout(self.layout)
