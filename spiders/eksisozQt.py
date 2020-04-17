import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import requests
import sys
import json
import eksisozluk.spiders.eksisoz

class pencere():
    def __init__(self):
        self.a = 1
        #pencere ayarlari
        app = QApplication(sys.argv)
        window = QWidget()
        window.setStyleSheet(open('style.qss').read())
        window.setWindowTitle("eksi soz")
        #giris cikis yerleri
        self.link = QLineEdit(window)
        self.link.setPlaceholderText("Link buraya ")
        self.link.setText('https://eksisozluk.com/dornaz-alfa--6477231?a=popular')
        #buton
        gonder_buttonu = QPushButton(window)
        gonder_buttonu.setText("Ara")
        gonder_buttonu.clicked.connect(self.Ara)
        gonder_buttonu.setDefault(True)
        # sekil = QLabel(window)
        # pixmap = QPixmap('resim.png')
        # sekil.setPixmap(pixmap)

        #duzen
        v_box = QVBoxLayout(window)
        resim_horizontal = QHBoxLayout(window)
        h2_box = QHBoxLayout(window)
        # resim_horizontal.addWidget(sekil)
        resim_horizontal.setAlignment(Qt.AlignCenter)
        h2_box.addWidget(self.link)
        v_box.addLayout(resim_horizontal)
        v_box.addLayout(h2_box)
        v_box.addWidget(gonder_buttonu)
        v_box.setAlignment(Qt.AlignTop)

        window.setLayout(v_box)

        #pencere sonu
        window.show()
        sys.exit(app.exec())
    #islemler
    def Ara(self):
        dialoq = QPlainTextEdit()
        QThread(eksisozluk.spiders.eksisoz.start(self.link.text()))
        dialoq.resize(800,800)
        info = open('info.json', 'r')
        info = json.load(info)
        entry_list = info[0]['entry']
        for i in entry_list:
            dialoq.insertPlainText(i+'\n')
            dialoq.insertPlainText(40*'#'+'\n')



        dialoq.show()


if __name__ =='__main__':
    pencere()


