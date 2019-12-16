import character
import skills.showSkill as showSkill
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from resource_path import *
from monsters import initial_monster
from level import *
import sys, time, threading, read_score, bgm
from monsters import monster_slime, monster_orange_mushroom, monster_ribbon_pig
import monsters.initial_monster


class Main(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.is_first_right = True
        self.is_first_left = True
        self.is_first_release_right = True
        self.is_first_release_left = True
        self.current_x = 0
        self.current_y = 0
        self.thread_end = False
        self.using_skill = False
        # initial mainWindow
        self.resize(1440, 627)
        self.setWindowTitle("Forest of Patience")
        self.setWindowIcon(QIcon("resource/maplestory.ico"))

        # background
        background_image = QImage(background[0])
        modified_background_image = background_image.scaled(QSize(2000, 1080))
        palette = QPalette()
        palette.setBrush(10, QBrush(modified_background_image))
        self.setPalette(palette)

        # ScoreDB_Read
        self.filename = 'score.dat'
        self.scoredb = []
        self.data = read_score.DB_Read(self.filename, self.scoredb)
        self.scoredb = self.data.readScoreDB()
        print(self.scoredb)
        self.start = False

        # Make Skill, Character
        self.skill = QLabel(self)
        self.character = QLabel(self)
        self.protect = QLabel(self)
        self.machine = QLabel(self)

        # highscore_out
        self.highscore = QLabel(self)
        self.highscore.setText('최고점수 : '+str(max(self.scoredb))+'점')
        self.highscore.move(800, 780)
        self.highscore.setFont(QFont("Arial", 40, QFont.Black))
        self.highscore.setStyleSheet("color:gold")

        # life
        self.life = QLabel(self)
        self.remaining_life = 100
        self.life.setText('보호대상의 체력 : ' + str(self.remaining_life) + ' / 100')
        self.life.setFont(QFont("Arial", 40, QFont.Bold))
        self.life.setStyleSheet("background-color: orange; color: white")
        self.life.move(10,20)
        self.life.setVisible(False)

        # currentScore
        self.current_score = QLabel(self)
        self.score = 0
        self.current_score.setText('현재 점수 : ' + str(self.score) + '점')
        self.current_score.setFont(QFont("Arial", 40, QFont.Bold))
        self.current_score.setStyleSheet("background-color: orange; color: white")
        self.current_score.move(10, 90)
        self.current_score.setVisible(False)

        # wave
        self.current_wave = QLabel(self)
        self.wave = 1
        self.current_wave.setText('Wave : ' + str(self.wave))
        self.current_wave.setFont(QFont("Arial", 40, QFont.Bold))
        self.current_wave.setStyleSheet("background-color: orange; color: black")
        self.current_wave.move(1670, 20)
        self.current_wave.setVisible(False)

        #title
        self.title = QLabel(self)
        self.title.move(500, 5)
        self.image = QPixmap("resource/title.png")
        self.title.setPixmap(self.image)

        # self.highscore.setVisible(True)
        # GameStart_btn
        self.gameStart_btn = QPushButton("게임 시작",self)
        self.gameStart_btn.move(500,500)
        self.gameStart_btn.resize(250, 150)
        self.gameStart_btn.setFont(QFont("Arial", 40, QFont.Bold))
        self.gameStart_btn.setStyleSheet("background-color: gold")
        self.gameStart_btn.clicked.connect(self.buttonEvent)
        self.close_btn = QPushButton("게임 종료", self)
        self.close_btn.move(1200, 500)
        self.close_btn.resize(250,150)
        self.close_btn.clicked.connect(self.buttonEvent)
        self.close_btn.setFont(QFont("Arial", 40, QFont.Bold))
        self.close_btn.setStyleSheet("background-color: gold")

    def gameStart(self):
        self.start = True
        self.gameStart_btn.setVisible(False)
        self.close_btn.setVisible(False)
        self.highscore.setVisible(False)
        self.current_score.setVisible(True)
        self.life.setVisible(True)
        self.current_wave.setVisible(True)
        self.title.setVisible(False)
        # skill
        # self.movie = self.movie = QMovie("resource/skill_6.gif", QByteArray(), self)
        # self.skill = QLabel(self)
        self.skill.setVisible(False)

        # character
        self.movie_character = QMovie(ch_stand, QByteArray(), self)
        # self.character = QLabel('', self)
        character.ch_initial(self, self.character, self.movie_character)
        self.character.move(100, 820)

        # protect
        self.movie_protect = QMovie(protect_2, QByteArray(), self)
        character.ob_initial(self, self.protect, self.movie_protect)

        # machine
        self.movie_machine = QMovie(machine_2, QByteArray(), self)
        character.mc_initial(self, self.machine, self.movie_machine)

        # Skill_icon
        self.skillicon = []
        self.cooltime = []
        self.cooltime_value = list(skill_dic.values())
        self.icon_x = 1700
        for i in range (len(skill_dic)):
            self.icon = QLabel(self)
            self.skillicon.append(self.icon)
            self.cool = QLabel(self)
            print(self.cooltime_value[i].getCoolTime)
            self.cool.setText(str(self.cooltime_value[i].getCoolTime()))
            self.cool.setFont(QFont("Arial", 40, QFont.Bold))
            self.cool.setStyleSheet("color: black")
            self.cooltime.append(self.cool)
            self.skillicon[i].move(self.icon_x, 120)
            self.skillicon[i].setVisible(True)
            self.cooltime[i].move(self.icon_x + 35, 145)
            self.cooltime[i].setVisible(True)
            self.image = QPixmap("resource/skill_icon_" + str(i + 1) + ".png")
            self.image = self.image.scaled(100, 100)
            self.skillicon[i].setPixmap(self.image)
            self.skillicon[i].resize(100, 100)
            self.icon_x += 100

        # threadings
        self.monster_list = []
        self.monster_image_list = [slime, orange_mushroom, ribbon_pig]
        slime_attribute = monsters.monster_slime.Slime()
        orange_mushroom_attribute = monsters.monster_orange_mushroom.OrangeMushroom()
        ribbon_pig_attribute = monsters.monster_ribbon_pig.RibbonPig()
        self.monster_attribute_class = [slime_attribute, orange_mushroom_attribute, ribbon_pig_attribute]

        # for i in range(5):
        #     m = QLabel(self)
        #     self.monster_list.append(m)
        is_first = False
        i = 1
        while i < 4:
            if not is_first:
                m = QLabel(self)
                mv = QMovie(self.monster_image_list[i-1], QByteArray(), self)
                initial_monster.slime(self, m, mv, i * 100 + 1400)
                self.monster_list.append(m)
                self.monsters_threads = threading.Thread(target=self.monster_thread)
                self.monsters_threads.start()
                i += 1
            # if self.monster_list[i].pos().x() < 1500:
            #     is_first = False
            #     i += 1

        # monster_create_thread = threading.Thread(target=self.monster_create)
        # monster_create_thread.start()



        self.barrier_thread = threading.Thread(target=self.barrier)
        self.barrier_thread.start()

    def monster_create(self):
        is_first = False
        i = 0
        while i < 5:
            if not is_first:
                mv = QMovie(self.monster_image_list[i], QByteArray(), self)
                initial_monster.slime(self, self.monster_list[i], mv)
                # self.monster_list.append(m)
                self.monsters_threads = threading.Thread(target=self.monster_thread)
                self.monsters_threads.start()
            if self.monster_list[i].pos().x() < 1500:
                is_first = False
                i += 1
                time.sleep(3)

    def monster_thread(self):
        dead_monster_count = 5
        while not self.thread_end:
            for i in range(len(self.monster_list)):
                if self.monster_attribute_class[i].hp <= 0:
                    self.monster_list[i].setVisible(False)

                if self.protect.pos().x() > self.monster_list[i].pos().x() - 50:
                    if self.monster_list[i].isVisible():
                        self.remaining_life -= 101
                        self.life.setText('보호대상의 체력 : ' + str(self.remaining_life) + ' / 100')
                    self.monster_list[i].setVisible(False)
                    # if self.remaining_life <= 0:
                        # TODO
                        # when protect id dead
                self.monster_list[i].move(self.monster_list[i].pos().x() - 5, self.monster_list[i].pos().y())
                time.sleep(0.05)

    def barrier(self):
        while not self.thread_end:
            if self.character.pos().x() <= 200:
                self.character.move(201, self.character.pos().y())
            elif self.character.pos().x() >= 1500:
                self.character.move(1499, self.character.pos().y())

    # def messi(self):
    #     while not self.thread_end:
    #         if self.protect.pos().x() > self.monster_orange_mushroom.pos().x() - 50:
    #             self.monster_orange_mushroom.setVisible(False)
    #             self.remaining_life -= 101
    #             self.life.setText('보호대상의 체력 : ' + str(self.remaining_life) + ' / 100')
    #             if (self.remaining_life <= 0):
    #                 self.protect.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    #                 self.protect.setAlignment(Qt.AlignCenter)
    #                 self.movie_orange_mushroom = QMovie(protect_2_dead, QByteArray(), self)
    #                 self.movie_orange_mushroom.setCacheMode(QMovie.CacheAll)
    #                 self.protect.setMovie(self.movie_orange_mushroom)
    #                 self.protect.resize(106, 75)
    #                 self.movie_orange_mushroom.start()
    #                 self.movie_orange_mushroom.loopCount()
    #                 print('game over')
    #                 # self.scoredb.append(self.score)
    #             break
    #         self.monster_orange_mushroom.move(self.monster_orange_mushroom.pos().x() - 5, self.monster_orange_mushroom.pos().y())
    #         time.sleep(0.05)
    #
    # def ronaldo(self):
    #     while not self.thread_end:
    #         if self.protect.pos().x() > self.monster_slime.pos().x()-50:
    #             self.monster_slime.setVisible(False)
    #             self.remaining_life -= 101
    #             self.life.setText('보호대상의 체력 : ' + str(self.remaining_life) + ' / 100')
    #             if self.remaining_life <= 0:
    #                 self.protect.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    #                 self.protect.setAlignment(Qt.AlignCenter)
    #                 self.movie_slime = QMovie(protect_2_dead, QByteArray(), self)
    #                 self.movie_slime.setCacheMode(QMovie.CacheAll)
    #                 self.protect.setMovie(self.movie_slime)
    #                 self.protect.resize(106, 75)
    #                 self.movie_slime.start()
    #                 self.movie_slime.loopCount()
    #                 print('game over')
    #                 #self.scoredb.append(self.score)
    #             break
    #         self.monster_slime.move(self.monster_slime.pos().x() - 5, self.monster_slime.pos().y())
    #         time.sleep(0.05)




    def buttonEvent(self,event):
        button = self.sender()
        key = button.text()
        if key == "게임 시작":
            self.gameStart()
        elif key == "게임 종료":
            self.close()

    def keyPressEvent(self, event):
        self.current_x = self.character.pos().x()
        self.current_y = self.character.pos().y()
        # right
        if event.key() == Qt.Key_D and not self.using_skill and self. start:
            if self.is_first_right:
                # initial character
                self.movie_character = QMovie(ch_walk, QByteArray(), self)
                character.ch_initial(self, self.character, self.movie_character)
                self.is_first_right = False
                self.is_first_left = True
                self.is_first_release_right = True
            self.character.move(self.current_x + 5, self.current_y)

        # left
        elif event.key() == Qt.Key_A and not self.using_skill and self. start:
            if self.is_first_left:
                # initial character
                self.movie_character = QMovie(ch_walk, QByteArray(), self)
                character.ch_initial(self, self.character, self.movie_character)
                self.is_first_right = True
                self.is_first_left = False
                self.is_first_release_left = True
            self.character.move(self.current_x - 5, self.current_y)

        else:
            showSkill.skill_activate(self, event, self.monster_list, self.monster_attribute_class, self.character)

        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        print(self.scoredb)
        self.thread_end = True
        self.data.writeScoreDB(self.scoredb)

    def keyReleaseEvent(self, event):
        self.current_x = self.character.pos().x()
        self.current_y = self.character.pos().y()
        key = event.key()
        # release right
        if key == 68 and not event.isAutoRepeat():
            if self.is_first_release_right and self.start and not self.using_skill:
                self.movie_character = QMovie(ch_stand, QByteArray(), self)
                character.ch_initial(self, self.character, self.movie_character)
                self.is_first_release_right = False
                self.is_first_right = True
                self.character.move(self.current_x, self.current_y)

        # release left
        elif key == 65 and not event.isAutoRepeat():
            if self.is_first_release_left and self.start:
                self.movie_character = QMovie(ch_stand, QByteArray(), self)
                character.ch_initial(self, self.character, self.movie_character)
                self.is_first_release_left = False
                self.is_first_left = True
                self.character.move(self.current_x, self.current_y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.showFullScreen()
    sys.exit(app.exec_())
