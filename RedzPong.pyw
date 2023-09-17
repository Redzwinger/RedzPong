from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import time
import subprocess

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RedzPong")
        self.setGeometry(310, 210, 1280, 720)
        self.setStyleSheet("background-color: rgb(242,242,172);")
        
        logo_widget = QWidget(self)
        logo_layout = QVBoxLayout(logo_widget)
        
        logo_label = QLabel(logo_widget)
        logo_pixmap = QPixmap("logo2.png")
        
        if logo_pixmap.isNull():
            print("Error: Unable to load the logo image.")
            
        else:
            logo_pixmap = logo_pixmap.scaled(200, 200, Qt.KeepAspectRatio)    
            logo_label.setPixmap(logo_pixmap)
            logo_widget.setGeometry(525, 40, 300, 300)
            
        presents = QLabel("Presents", logo_widget)
        presents.setGeometry(425, 40, 300, 300)
        presents.setFont(QFont('Press Start 2P', 15))
        
        PongTitle = QLabel("RedzPong", self)
        PongTitle.setGeometry(345, 320, 600, 200)
        PongTitle.setFont(QFont('Press Start 2P', 45))
        

        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(presents)
        
        Srtbtn = QPushButton('Press Start', self)
        Srtbtn.setGeometry(435, 520, 400, 110)
        Srtbtn.setFont(QFont('Press Start 2P', 20))
        Srtbtn.setToolTip("<b>;)</b>")  
        
        Srtbtn.clicked.connect(self.launchOtherScript)

        qbtn = QPushButton("Quit", self)
        qbtn.setGeometry(560, 640, 150, 50)
        qbtn.setToolTip("Aww, you're leaving already? <b>:(</b>")
        qbtn.setFont(QFont('Press Start 2P', 12))
        qbtn.clicked.connect(QApplication.instance().quit)

        QToolTip.setFont(QFont('Expansive', 8))

        self.show()

    def launchOtherScript(self):
        self.other_process = QProcess()
        self.other_process.start('pythonw', ['NEAT_AI_the_less_ego_hurting_version.py'])
        self.other_process.finished.connect(self.handleOtherScriptFinished)

    def handleOtherScriptFinished(self):
        self.other_process.deleteLater()
        self.show()

class MovieSplashScreen(QSplashScreen):

    def __init__(self, movie, parent=None):
        movie.jumpToFrame(0)
        pixmap = QPixmap(movie.frameRect().size())

        QSplashScreen.__init__(self, pixmap)
        self.movie = movie
        self.movie.frameChanged.connect(self.repaint)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)

if __name__ == "__main__":
    I_am_newer = QApplication(sys.argv)
    
    movie = QMovie("splashshortrdz.gif")
    
    splash = MovieSplashScreen(movie)
    splash.show()
    splash.movie.start()
    splash.show()
    
    start = time.time()

    while movie.state() == QMovie.Running and time.time() < start + 4:
        I_am_newer.processEvents()

    window = MainWindow()
    window.show()
    splash.finish(window)

    sys.exit(I_am_newer.exec())
