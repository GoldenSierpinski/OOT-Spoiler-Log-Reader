import os
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from Fonts import getFont

class Item:
    def __init__(self,item,image):
        if isinstance(item,dict):
            self.name = item['item']
        else:
            self.name = item
        self.image = image
        self.location = []
        self.tab = ''

    def createItemLabel(self):
        itemLabel = QLabel()
        itemLabel.setMinimumHeight(32)
        if self.image is not None and os.path.isfile("./assets/" + self.image):
            pixmap = QPixmap("./assets/" + self.image)
            pixmap.scaled(itemLabel.size(), Qt.KeepAspectRatio)
            itemLabel.setPixmap(pixmap)
        else:
            itemLabel.setText(self.name)
            itemLabel.setFixedHeight(32)
            font = getFont('label')
            itemLabel.setFont(font)
        return itemLabel





