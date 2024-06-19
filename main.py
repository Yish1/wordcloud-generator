import os
import sys
import time
import jieba
import chardet
import gettext
import requests
import wordcloud
import numpy as np
from PIL import Image
from bs4 import BeautifulSoup
# import ptvsd  # QThread断点工具
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from fontTools.ttLib import TTFont, TTCollection
from ui import Ui_MainWindow, select_font, CustomDialog, Language_select  # 导入ui文件
from PyQt5.QtCore import QThreadPool, pyqtSignal, QRunnable, QObject, QCoreApplication
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QMessageBox, QApplication, QWidget
# 初始化jieba字典
jieba.set_dictionary(".\dict.txt")
jieba.initialize()
# 全局变量
version = "1.3"
is_selected_font = 0
dafault_image = 0
save_font = ""
bgimage = None

try:
    with open('language.ini', 'r') as file:
        language_value = str(file.read())
    localedir1 = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'locale')
    translate = gettext.translation(
        domain=f"{language_value}", localedir=localedir1, languages=[f"{language_value}"])
    _ = translate.gettext
except:
    localedir1 = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'locale')
    translate = gettext.translation(
        domain="zh_CN", localedir=localedir1, languages=["zh_CN"])
    _ = translate.gettext


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.lineEdit.setText("https://")
        self.label.setText(_("\n\n\n欢迎使用网页词云生成器！\n"
                             "在上方文本框中输入需要分析的网址\n"
                             "(需要输入http://或https://协议头)，\n"
                             "\n"
                             "点击开始按钮，稍后即可在右栏中查看词云。\n\n\n"))
        self.pushButton.setText(_("开始生成词云图"))
        self.menu.setTitle(_("设置"))
        self.menu_2.setTitle(_("保存"))

        self.actionSave = QtWidgets.QAction(_("保存词云图"), MainWindow)
        self.setbg = QtWidgets.QAction(_("词云形状"), MainWindow)
        self.setfont = QtWidgets.QAction(_("词云字体"), MainWindow)
        self.custimg = QtWidgets.QAction(_("使用自定义文字生成词云"), MainWindow)
        self.actionabout = QtWidgets.QAction(_("关于此工具"), MainWindow)
        self.setlang = QtWidgets.QAction(_("语言"), MainWindow)
        self.menu_2.addAction(self.actionSave)
        self.menu.addAction(self.setbg)
        self.menu.addAction(self.setfont)
        self.menu.addAction(self.custimg)
        self.menu.addSeparator()
        self.menu.addAction(self.setlang)
        self.menu.addAction(self.actionabout)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 定义按钮功能
        self.setWindowTitle(QCoreApplication.translate(
            "MainWindow", _("网页词云生成器 %s") % version))
        self.pushButton.clicked.connect(self.start_process)
        self.lineEdit.returnPressed.connect(self.trigger_button_click)
        self.custimg.triggered.connect(self.cust_img)
        self.actionSave.triggered.connect(self.saveimage)
        self.setlang.triggered.connect(self.set_lang)
        self.actionabout.triggered.connect(self.about_tool)
        self.setfont.triggered.connect(self.set_Font)
        self.setbg.triggered.connect(self.set_bg)
        if dafault_image == 0:
            self.set_default_image()
        else:
            pass

    def closeEvent(self, event):
        # 关闭其他窗口的代码
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QWidget) and widget != self:
                widget.close()
        event.accept()

    def saveimage(self):
        if dafault_image == 1:
            print("保存随机图")
            filename, f = QtWidgets.QFileDialog.getSaveFileName(
                None, _("保存api随机图片"), "./savewc", _("来自沉梦小站的随机图API图片 (*.png *.jpg *.webp)"))
            if filename:
                image = QtGui.QImage(
                    self.graphicsView.scene().items()[0].pixmap())
                image.save(filename)
                print("api图片已保存至:", filename)
        else:
            print("保存图云")
            filename, f = QtWidgets.QFileDialog.getSaveFileName(
                None, _("保存词云图"), "./savewc", _("来自网页词云生成工具 (*.png)"))
            if filename:
                image = QtGui.QImage(
                    self.graphicsView.scene().items()[0].pixmap())
                image.save(filename)
                print("词云已保存至:", filename)

    def cust_img(self):
        # 自定义文本
        self.dialog = CustomDialog_1()
        self.dialog.show()
        self.dialog.custom_start_button.clicked.connect(
            lambda: self.start_ana_text(self.dialog.cust_text.toPlainText()))
        # 连接按钮

    def start_ana_text(self, cust_text):
        if cust_text == "":
            self.show_message(_("请输入有效内容！！！"), _("错误"))
        else:
            with open('urlciyun_temp.txt', 'w', encoding="utf8") as file:
                file.write(cust_text)
            self.start_process(1)
            self.dialog.custom_start_button.setEnabled(False)

    def set_lang(self):
        print("打开语言设置")
        lang = Language_select_1()
        lang.exec_()

    def set_Font(self):
        global is_selected_font
        is_selected_font = 1
        print("打开字体设置")
        sf = select_font_1()
        sf.showFontDialog()

    def set_bg(self):
        global bgimage, dafault_image  # 遮罩图片
        # 默认由image文件夹存放遮罩图片
        bgimage, f = QtWidgets.QFileDialog.getOpenFileName(
            None, _("选择图片文件"), "./images", _("图片文件 (*.png *.jpg *.jpeg *.webp)"))
        if bgimage:
            print("选择的文件路径：", bgimage)
            try:
                wc_pixmap = QPixmap(bgimage)
                wc_item = QGraphicsPixmapItem(wc_pixmap)
                wc_item.setScale(0.14)
                wc_scene = QGraphicsScene()
                wc_scene.addItem(wc_item)
                self.update_graphics_view(wc_scene)
                self.label.setText(
                    _("您选择了%s作为词云图形状\n\nTips: 尽可能选择分辨率较高且背景为白色的图片，所选图片分辨率即为词云图分辨率！\n\n正常情况下，您应该可以在右栏看到选择的图片，如果没有正常显示，则图片无法读取，尝试更换图片！") % bgimage)
                dafault_image = 0
            except Exception as e:
                self.show_message(e, _("错误"), 1)
        else:
            print("未选择文件")

    def about_tool(self):
        print("打开关于")
        msgBox = QMessageBox()
        msgBox.setWindowIcon(QIcon('wc.ico'))
        msgBox.setWindowTitle(_("网页词云生成器"))
        msgBox.setText(_("感谢您使用网页词云生成器！\n\n这是一个作为Py课设的小工具，使用Pyqt5搭建ui，request、bs4和jieba分析网页内容，"
                       "再使用wordcloud生成词云。\n\n除此之外，还第一次尝试了多线程等性能优化方式，使用Qthread遇到了不少麻烦，比如无法结束线程，内存泄漏等，后面换用线程池(可以自动结束线程)解决了。\n\n"
                         "不过即便是这样一个小程序，也依旧还有许多的不足（比如MSN和百度系列的网站无法分析），也有许多尚未实现的想法。此工具将会开源，以及在沉梦小站中分享一些遇到的问题及解决方法。\n\n"
                         "作者：Yish_\n\n版本：%s\n\n注：此工具调用了沉梦小站的随机图api") % version)
        msgBox.setIconPixmap(QIcon('wc.ico').pixmap(64, 64))
        msgBox.exec_()

    def set_default_image(self):
        self.threadpool = QThreadPool()
        # 将获取随机图移至子线程
        worker = GetDefaultPicture()
        worker.signals.update_graphics_view.connect(self.update_graphics_view)
        self.threadpool.start(worker)

    def start_process(self, custom=None):
        url = self.lineEdit.text()
        if custom is None or custom is False:
            self.thread = WorkerThread(url)
        else:
            self.thread = WorkerThread(None, 1)
            # 传输参数1时，代表使用的是自定义文本模式
        self.thread.signals.progress_changed.connect(self.update_progress_bar)
        self.thread.signals.update_label.connect(self.update_label)
        self.thread.signals.enable_button.connect(self.enable_button)
        self.thread.signals.show_message.connect(self.show_message)
        self.thread.signals.set_Font.connect(self.set_Font)
        self.thread.signals.update_graphics_view.connect(
            self.update_graphics_view)
        self.thread.signals.update_pushbotton.connect(self.update_pushbotton)
        self.pushButton.setEnabled(False)
        self.progressBar.show()
        self.thread.signals.finished.connect(self.progressBar.hide)
        self.threadpool.start(self.thread)

    def update_progress_bar(self, value):
        self.progressBar.setValue(value)

    def update_pushbotton(self, text):
        self.pushButton.setText(text)

    def update_label(self, text):
        if not text or not text.strip() or text.strip(" .") == "":
            self.label.setText(_("没有在此页面获取到有效信息！"))
        else:
            self.label.setText(text)

    def enable_button(self):
        self.pushButton.setEnabled(True)
        try:
            self.dialog.custom_start_button.setEnabled(True)
        except:
            pass

    def show_message(self, message, title, mode=None):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        if message is None:
            message = "未知错误"
        message = str(message)
        msgBox.setText(message)
        msgBox.exec_()
        if mode is None:
            self.pushButton.setText(_("开始生成词云图"))
            self.progressBar.hide()
        elif mode == 1:
            pass

    def update_graphics_view(self, scene):
        self.graphicsView.setScene(scene)


class select_font_1(select_font):
    def showFontDialog(self):
        self.selected_font_path = ""
        super().showFontDialog()
        self.dialog.setWindowTitle("选择词云字体")
        self.ok_button.setText(_("确定"))
        self.ok_button.clicked.connect(self.accept_font)
        self.fontComboBox.currentFontChanged.connect(self.updateFontPreview)
        self.ok_button.setEnabled(False)
        self.dialog.exec_()

    def accept_font(self):
        global save_font
        save_font = self.selected_font_path
        print(f"已保存字体设置{save_font}")
        self.dialog.accept

    def updateFontPreview(self, font):
        super().updateFontPreview(font)
        self.a = MainWindow
        font_name = font.family()
        result, self.selected_font_path = 0, ""
        print(f"选择了{font_name}字体")
        try:
            try:
                font_dir = os.path.expanduser(
                    "~") + r'\AppData\Local\Microsoft\Windows\Fonts'
                result, self.selected_font_path = self.find_ttf_name(
                    font_dir, font_name)
            except:
                self.a.show_message(self, _("暂不支持Windows7及以下系统！"), _("错误"), 1)
                # win7字体文件不在此目录下，问就是懒得找了。
            if result != 1:
                result, self.selected_font_path = self.find_ttf_name(
                    r'C:\Windows\Fonts', font_name)
            if self.selected_font_path == "":
                self.a.show_message(
                    self, _("无法找到此字体的实际地址\n请尝试更换其他字体！"), _("无法设置字体"), 1)
                # QT字体选择组件返回的是字体family名，而wordcloud只接受字体的实际文件路径
                # 因此需要重新对应字体名与实际文件位置
                self.ok_button.setEnabled(False)
        except Exception as e:
            self.a.show_message(self, e, _("错误"), 1)

    def find_ttf_name(self, font_dir, select_name=None):
        # 遍历字体文件目录下的所有 .ttf 文件
        for file_name in os.listdir(font_dir):
            if file_name.lower().endswith('.ttf') or file_name.lower().endswith('.otf'):
                self.selected_font_path = os.path.join(font_dir, file_name)
                # 读取字体文件ttf/otf
                try:
                    font = TTFont(self.selected_font_path)
                except:
                    continue
                # 获取字体元数据
                metadata = font['name']
                for record in metadata.names:
                    if record.nameID >= 0:
                        try:
                            name = record.toUnicode()
                        except UnicodeDecodeError:
                            name = record.string
                        if select_name == None:
                            pass
                        elif select_name == name:
                            font.close()
                            print(_("找到字体%s, %s") %
                                  (name, self.selected_font_path))
                            self.ok_button.setEnabled(True)
                            result = 1
                            return result, self.selected_font_path
                    else:
                        pass
                font.close()
            elif file_name.lower().endswith('.ttc'):
                self.selected_font_path = os.path.join(font_dir, file_name)
                result, self.selected_font_path = self.process_ttc_font(
                    select_name)
                if result == 1:
                    return result, self.selected_font_path
            else:
                pass
        return 0, ""

    def process_ttc_font(self, select_name=None):
        # 读取字体集合文件ttc
        try:
            font_collection = TTCollection(self.selected_font_path)
        except:
            pass
        # 遍历字体集合中的每个子字体
        for f, font in enumerate(font_collection):
            metadata = font['name']
            for record in metadata.names:
                if record.nameID >= 0:
                    try:
                        name = record.toUnicode()
                    except UnicodeDecodeError:
                        name = record.string
                    if select_name == None:
                        pass
                    elif select_name == name:
                        print(_("找到字体%s, %s") %
                              (name, self.selected_font_path))
                        self.ok_button.setEnabled(True)
                        result = 1
                        font.close()
                        font_collection.close()
                        return result, self.selected_font_path
        font.close()
        font_collection.close()
        return 0, ""


class CustomDialog_1(CustomDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(_("使用自定义文本生成词云图"))
        self.cust_text.setPlainText(_("""未行之路:
                                    在你消失的夜里穿行 
                                    微风送来最后一封信 
                                    通篇找寻沉默的音讯 
                                    谜底也许  不期而遇 
                                    
                                    悲欢离合是旅行的考卷 
                                    明月下想象另一轮明月 
                                    假如某刻你我再次相见 
                                    过往 能否重现 
                                    故事 再向前 
                                    
                                    我从未原地等待 
                                    追赶命运的节拍 
                                    夜幕深如海 而你照亮远方之外 
                                    无论海角天涯 你找到我出发
                                    前路无阻 就算一切崩塌 
                                    
                                    当白雪渐渐消融 
                                    当坚冰显现裂缝 
                                    而你是否已经扬帆启航 乘着风 
                                    无论海角天涯 我找到你出发
                                    我们从未迷路 
                                    我们终将重逢"""))
        self.custom_start_button = QtWidgets.QPushButton(_("开始生成词云图"), self)
        self.layout.addWidget(self.custom_start_button)


class Language_select_1(Language_select):
    def __init__(self):
        super().__init__()
        self.a = MainWindow()
        self.setWindowTitle(_("选择语言"))
        self.populateComboBox()
        self.langok_button = QtWidgets.QPushButton(_("确定"), self)
        self.langok_button.setMinimumHeight(40)
        self.layout.addWidget(self.langok_button)
        self.langok_button.clicked.connect(self.change_lang)

    def populateComboBox(self):
        # 读取指定目录下的文件夹名
        locale_dir = "./locale"
        try:
            if os.path.exists(locale_dir) and os.path.isdir(locale_dir):
                folders = [folder for folder in os.listdir(
                    locale_dir) if os.path.isdir(os.path.join(locale_dir, folder))]
                self.comboBox.addItems(folders)
        except Exception as e:
            print(f"读取语言失败:{e}")

    def change_lang(self):
        locale = self.comboBox.currentText()
        print(locale)
        try:
            with open('language.ini', 'w', encoding="utf8") as file:
                file.write(locale)
            self.a.show_message(_("修改语言后重启程序生效"), _("提示"), 1)

        except Exception as e:
            print(f"修改语言失败:{e}")
            self.a.show_message(e, _("错误"), 1)


class WorkerSignals(QObject):
    # 定义信号
    progress_changed = pyqtSignal(int)
    update_label = pyqtSignal(str)
    update_pushbotton = pyqtSignal(str)
    enable_button = pyqtSignal()
    show_message = pyqtSignal(str, str)
    update_graphics_view = pyqtSignal(object)
    finished = pyqtSignal()
    set_Font = pyqtSignal()


class GetDefaultPicture(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()

    def run(self):
        # ptvsd.debug_this_thread()  # 在此线程启动断点调试
        global dafault_image
        try:
            url = "https://cmxz.top/images/api/api.php"
            response = requests.get(url, timeout=3)
            if response.text == "访问太频繁，服务器要炸":
                raise requests.exceptions.Timeout
            if response.status_code != 200:
                raise requests.exceptions.Timeout
            img_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)
            item = QGraphicsPixmapItem(pixmap)
            item.setScale(0.14)
            scene = QGraphicsScene()
            scene.addItem(item)
            self.signals.update_graphics_view.emit(scene)
            print("获取随机图成功")
            dafault_image = 1
        except requests.exceptions.Timeout:
            # 请求超时，使用 wc.png
            wc_pixmap = QPixmap("wc.png")
            wc_item = QGraphicsPixmapItem(wc_pixmap)
            wc_item.setScale(0.14)
            wc_scene = QGraphicsScene()
            wc_scene.addItem(wc_item)
            self.signals.update_graphics_view.emit(wc_scene)
            print("请求超时，使用 wc.png")
        except Exception as e:
            # 其他错误
            wc_pixmap = QPixmap("wc.png")
            wc_item = QGraphicsPixmapItem(wc_pixmap)
            wc_item.setScale(0.14)
            wc_scene = QGraphicsScene()
            wc_scene.addItem(wc_item)
            self.signals.update_graphics_view.emit(wc_scene)
            print("获取随机图失败:%s，使用 wc.png" % e)

        self.setAutoDelete(True)
        # 启用自动删除子线程


class WorkerThread(QRunnable):
    def __init__(self, url=None, custom=None):
        super().__init__()
        self.signals = WorkerSignals()
        self.scene = None
        self.url = url
        self.save_font = save_font
        self.custom = custom

    def run(self):
        # ptvsd.debug_this_thread()  # 在此线程启动断点调试

        def update_progress_bar(old, new, speed=None):  # 进度条初始值，目标值，速度
            if speed is None:
                speed = 0.02  # 默认速度
            for i in range(old, new + 1):
                self.signals.progress_changed.emit(i)
                time.sleep(speed)

        def get_web_text():
            def is_content_valid(content):
                # 检查获取的内容是否有效，是否包含常见的汉字或可打印字符
                if any('\u4e00' <= char <= '\u9fff' for char in content):  # 检查是否包含汉字
                    return True
                if all(32 <= ord(char) <= 126 for char in content):  # 检查是否全为可打印字符
                    return True
                return False

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
            }
            urldata = None
            content = None
            error = False
            try:
                urldata = requests.get(self.url, headers=headers, verify=True)
                detected_encoding = chardet.detect(urldata.content)['encoding']
                # 根据检测到的编码设置编码
                urldata.encoding = detected_encoding
                content = urldata.text
                # 如果检测到的编码解码失败或结果乱码，尝试常见的编码
                if not content or not is_content_valid(content):
                    for encoding in ['utf-8', 'gbk']:
                        try:
                            urldata.encoding = encoding
                            content = urldata.text
                            if is_content_valid(content):
                                print(_("尝试在此页面使用%s编码") % encoding)
                                break
                        except:
                            continue
                else:
                    print(_("此页面使用%s编码") % detected_encoding)
                    pass

            except requests.exceptions.SSLError:
                transmit_message(
                    _("网站SSL证书不存在或者失效，可能导致无法访问或者使您的设备遭受攻击。\n若仍要继续访问，请去除链接\'https\'中的\'s\'。"), _("警告"))
                error = True
            except requests.exceptions.RequestException as e:
                error_message = _("请输入可访问的网址！！！\n%s") % e
                transmit_message(error_message, _("错误"))
                error = True
            return content if content else None, error

        def save_into_file(data):
            try:
                with open('urlciyun_temp.txt', 'w', encoding="utf8") as file:
                    file.write(data)
            except Exception as e:
                print(_("保存url文本出错: %s") % e)

        def make_wc():
            global dafault_image, is_selected_font, bgimage
            try:
                path = "urlciyun_temp.txt"
                if is_selected_font == 1:
                    font = save_font
                    # 默认使用方正舒体，但也有电脑没这个字体(被精简掉了)
                    if font == "" or font is None:
                        font = r'C:\Windows\Fonts\FZSTK.TTF'
                else:
                    font = r'C:\Windows\Fonts\FZSTK.TTF'
                try:
                    if os.path.exists(font):
                        pass
                    else:
                        raise FileNotFoundError(
                            "Your computer does not have FZSTK.TTF font.")
                except FileNotFoundError as e:
                    self.signals.set_Font.emit()
                    transmit_message(_("请选择一个用于生成词云图的字体！\n%s") %
                                     e, _("请先选择字体！"))
                    return
                print(f"本次词云图使用{font}字体生成")

                def tcg(texts):
                    cut = jieba.cut(texts)  # 分词
                    string = ' '.join(cut)
                    return string
                text = (open(path, 'r', encoding='utf-8')).read()
                string = tcg(text)
                if bgimage is None or bgimage == "":
                    img_array = None
                else:
                    with Image.open(bgimage) as image:
                        img_array = np.array(image)
                with open("stopword.txt", encoding='utf8') as f:
                    stopword = set(line.strip('\n') for line in f.readlines())
                    if self.url == "https://cmxz.top":
                        stopword.update(["热度", "评论", "AI"])
                wc = wordcloud.WordCloud(
                    background_color='white',
                    scale=2,
                    # 貌似1280x720再放大两倍生成速度比直接2k速度快一点
                    width=1280,
                    height=720,
                    mask=img_array,  # 设置背景图片
                    font_path=font,
                    stopwords=stopword
                )
                wc.generate_from_text(string)  # 绘制图片
                wc.to_file("wordcloud.png")  # 保存图片
                pixmap = QPixmap()
                pixmap.load("wordcloud.png")
                item = QGraphicsPixmapItem(pixmap)
                self.scale = 0.18
                item.setScale(self.scale)
                self.scene = QGraphicsScene()
                self.scene.addItem(item)
                self.signals.update_graphics_view.emit(self.scene)
                dafault_image = 0
            except Exception as e:
                transmit_message(_("生成词云图出错: %s") % e, _("错误"))

        def transmit_message(text, title=None):
            if title is None:
                title = _("提示")
            self.signals.show_message.emit(text, title)

        def stop():
            self.signals.progress_changed.emit(0)
            self.signals.update_pushbotton.emit(_("词云图生成完毕"))
            self.signals.enable_button.emit()  # 启用按钮
            self.signals.update_pushbotton.emit(_("开始生成词云图"))
            self.signals.finished.emit()
            # 向主线程发送终止信号

        # run
        if self.custom == 1:
            # 自定义模式
            self.signals.update_pushbotton.emit(_("词云图装载中...\n正在分析文本..."))
            update_progress_bar(0, 20)
            self.signals.update_pushbotton.emit(
                _("词云图装载中...\n(正在生成词云图，卡顿是正常现象)"))
            update_progress_bar(20, 50)
            make_wc()
            update_progress_bar(50, 100, 0.01)
            stop()
            self.setAutoDelete(True)
            return

        text, error = get_web_text()
        if text is None:
            if error:
                pass
            else:
                transmit_message(_("网页无法访问，请检查链接是否正确！"), _("错误"))
            stop()
            return
        self.signals.update_pushbotton.emit(_("词云图装载中...\n正在尝试访问网站..."))
        update_progress_bar(0, 20)
        soup = BeautifulSoup(text, "html.parser")

        title = soup.title.string if soup.title else None
        a = _("标题: ") + title + "\n\n" if title else ""

        description = soup.find('meta', attrs={'name': 'description'})
        b = _("网站简介:") + description['content'] + "\n" if description else ""

        c = a + b
        self.signals.update_label.emit(c)

        text = soup.get_text()
        text = text.replace('\n', ' ')
        update_progress_bar(20, 50)
        self.signals.update_pushbotton.emit(_("词云图装载中...\n(正在生成词云图，卡顿是正常现象)"))
        save_into_file(text)
        make_wc()
        update_progress_bar(50, 100, 0.01)
        stop()
        self.setAutoDelete(True)


if __name__ == "__main__":
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(
            QtCore.Qt.AA_EnableHighDpiScaling, True)
    # 启用高DPI自适应
    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(
            QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
