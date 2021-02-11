from PyQt5.QtWidgets import QLineEdit
from Fonts import getFont

class Region:
    def __init__(self,region,regionInfo):
        self.name = region
        self.search = regionInfo['search']
        self.isDungeon = regionInfo['dungeon']
        self.locations = []
        self.entrances = []
        self.exits = []
        self.isMQ = False

        if self.isDungeon:
            if self.name in ('Ice Cavern','Bottom of the Well','Gerudo Training Grounds','Ganons Castle'):
                self.dungeonType = 'Minor'
            else:
                self.dungeonType = 'Major'
        else:
            self.dungeonType = None

    def createRegionBox(self):
        regionBox = QLineEdit()
        regionBox.setReadOnly(True)
        regionBox.setFixedHeight(32)
        font = getFont('box')
        regionBox.setFont(font)

        displayText = self.name
        if self.dungeonType is not None:
            if self.dungeonType == 'Major':
                if self.isMQ:
                    displayText = '[MQ] ' + displayText
            elif self.dungeonType == 'Minor':
                if self.isMQ:
                    displayText = 'Master Quest'
                else:
                    displayText = 'Vanilla'

        regionBox.setText(displayText)

        return regionBox