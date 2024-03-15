from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt6.QtGui import QIcon, QMovie
from re import split

from src.layout import Ui_Widget

from Aliex.Aliexpress_Products import Aliex_main_id

class BGMainUi(QWidget):
  def __init__(self):
    # super().__init__()
    super().__init__()
    self.ui = Ui_Widget()
    self.ui.setupUi(self)
    self.initUI()

  def initUI(self):
    # Set the window's title
    self.setWindowTitle('Aliexpress ツール')
    app_icon = QIcon('img/icon.ico')
    self.setWindowIcon(app_icon)
    self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint)
    self.setstyle_setting()
    self.btn_event()

    # Set the background color of the main widget
    self.setAutoFillBackground(True)
    p = self.palette()
    p.setColor(self.backgroundRole(), Qt.GlobalColor.white)  # Replace with the desired color
    self.setPalette(p)

  def btn_event(self):
    self.ui.startButton.clicked.connect(self.get_dataset)

  def setstyle_setting(self):
    self.movie = QMovie('img/loading.gif')
    self.ui.label_loading.setMovie(self.movie)
    self.movie.start()
    self.ui.label_loading.hide()

  def get_dataset(self):
    self.thread = WorkerThread(self.ui)
    self.thread.finished.connect(self.on_thread_get_finished)
    self.thread.error.connect(self.show_warning_message)
    self.thread.start()
    self.ui.label_loading.show()
    self.ui.startButton.hide()
  
  def on_thread_get_finished(self, result):
    self.ui.label_loading.hide()
    self.ui.startButton.show()
    ms = QMessageBox()
    ms.setIcon(QMessageBox.Icon.Information)
    ms.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
    if (result == '\"error\"' or result == 'error' or result == 'No products found'):
      ms.setText("エラーが発生しました。数分後に再度実行してください。")
      ms.setWindowTitle("エラー")
    else:
      ms.setText("完了しました。")
      ms.setWindowTitle("完了")
    ms.setWindowIcon(QIcon('img/icon.ico'))
    ms.exec()
    print('終了しました。')
  
  def show_warning_message(self, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setText(message)
    msg.setWindowTitle("エラー")
    msg.setWindowIcon(QIcon('img/icon.ico'))
    msg.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
    self.ui.label_loading.hide()
    self.ui.startButton.show()
    msg.exec()

  def closeEvent(self, event):
    print("Closed!")  
  
class WorkerThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
    def run(self):

      # Get the text from textEdit2
      ng_words_string = self.ui.textEdit3.toPlainText()  # Get the text from textEdit3
      if ng_words_string == "":
        ng_words = []
      else:
        ng_words = split(r'[,\s　、]+', ng_words_string)
      
      print('ng_words ', ng_words)
      status_Aliex_blon = Aliex_main_id(ng_words)
      # print('Result: ', status_Aliex_blon)
      self.finished.emit(status_Aliex_blon)

if __name__ == '__main__':

  import sys
  app = QApplication(sys.argv)

  window = BGMainUi()
  window.show()
  sys.exit(app.exec( ))