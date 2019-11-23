from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from block import Block
import sys



class Main(QWidget):
    is_first_right = True
    is_first_left = True
    def __init__(self, title, gif_file, parent=None):
        QWidget.__init__(self, parent)

        # initial mainWindow
        self.resize(1046, 3772) # original 1046 x 3772
        self.setWindowTitle("Forest of Patience")

        # create main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # background
        background_image = QImage('resource/back_ground_1.png')
        modified_background_image = background_image.scaled(QSize(1046, 3772)) # original 1046 x 3772
        palette = QPalette()
        palette.setBrush(10, QBrush(modified_background_image))
        self.setPalette(palette)

        # blocks
        block = Block(10, 10)
        main_layout.addWidget(block)

        # character
        self.movie = QMovie(gif_file, QByteArray(), self)
        self.character = QLabel()
        self.character.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.character.setAlignment(Qt.AlignCenter)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.character.setMovie(self.movie)
        self.movie.start()
        self.movie.loopCount()
        main_layout.addWidget(self.character)


    def keyPressEvent(self, e):
        print("keyInput : ", self.character.pos().x(), self.character.pos().y())
        # right
        if e.key() == Qt.Key_D:
            print("before : ", self.character.pos().x(), self.character.pos().y())
            if self.is_first_right:
                # initial character
                self.movie = QMovie('resource/avatar_walk1_default_flip.gif', QByteArray(), self)
                self.character.setMovie(self.movie)
                self.movie.start()
                self.movie.loopCount()
                self.is_first_right = False
                self.is_first_left = True
                print("ing : ", self.character.pos().x(), self.character.pos().y())

            self.character.move(self.character.pos().x() + 5, self.character.pos().y())
            print("after : ", self.character.pos().x(), self.character.pos().y())

        # left
        elif e.key() == Qt.Key_A:
            if self.is_first_left:
                # initial character
                self.movie = QMovie('resource/avatar_walk1_default.gif', QByteArray(), self)
                self.character.setMovie(self.movie)
                self.character.move(self.character.pos().x(), self.character.pos().y())
                self.movie.start()
                self.movie.loopCount()
                self.is_first_left = False
                self.is_first_right = True

            self.character.move(self.character.pos().x() - 5, self.character.pos().y())
            print(self.character.pos().x(), self.character.pos().y())


        # up
        elif e.key() == Qt.Key_W:
            self.character.move(self.character.pos().x(), self.character.pos().y() - 5)
            print(self.character.pos().x(), self.character.pos().y())

        # down
        elif e.key() == Qt.Key_S:
            self.character.move(self.character.pos().x(), self.character.pos().y() + 5)
            print(self.character.pos().x(), self.character.pos().y())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main("update this gif", "resource/avatar_walk1_default.gif")
    main.show()
    sys.exit(app.exec_())