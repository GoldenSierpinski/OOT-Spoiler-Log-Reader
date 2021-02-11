from PyQt5.QtWidgets import QLabel, QLineEdit
from Fonts import getFont

class Entrance:
    def __init__(self,entrance,location):
        path = entrance.split(' -> ')
        self.entrance = entrance
        self.location = location

        self.entranceFrom = path[0]
        self.entranceTo = path[1]
        if isinstance(location,dict):
            self.leadsToRegion = location['region']
            self.leadsFromRegion = location['from']
            self.isInterior = False
        else:
            self.leadsToRegion = location
            self.leadsFromRegion = 'Interior'
            self.isInterior = True

        self.isOwl = False
        self.isWarpSong = False
        self.isDungeon = False
        self.isSpawn = False

        if 'Owl' in self.entranceFrom:
            self.isOwl = True
        elif 'Warp' in self.entranceFrom and 'Woods' not in self.entranceFrom and 'Graveyard' not in self.entranceFrom:
            self.isWarpSong = True
        elif 'Adult Spawn' in self.entranceFrom or 'Child Spawn' in self.entranceFrom:
            self.isSpawn = True

    def createEnteringRegionLabels(self):
        # Label should be "From" + leads from region. If interior, then label should be leadsTo
        # Box should be entrance text
        dungeons = {'Deku Tree Lobby': 'Deku Tree',
                    'Dodongos Cavern Beginning': 'Dodongo\'s Cavern',
                    'Jabu Jabus Belly Beginning': 'Jabu\'s Jabu Belly',
                    'Forest Temple Lobby': 'Forest Temple',
                    'Fire Temple Lower': 'Fire Temple',
                    'Water Temple Lobby': 'Water Temple',
                    'Shadow Temple Entryway': 'Shadow Temple',
                    'Spirit Temple Lobby': 'Spirit Temple',
                    'Ice Cavern Beginning': 'Ice Cavern',
                    'Bottom of the Well': 'Bottom of the Well',
                    'Gerudo Training Grounds Lobby': 'Gerudo Training Grounds'}

        if self.leadsToRegion in dungeons:
            entranceText = dungeons[self.leadsToRegion]
        elif self.isInterior:
            entranceText = self.leadsToRegion
        else:
            entranceText = 'From ' + self.leadsFromRegion

        entranceLabel = QLabel(entranceText)
        entranceLabel.setMinimumHeight(32)
        font = getFont('label')
        entranceLabel.setFont(font)

        entranceBox = QLineEdit()
        entranceBox.setReadOnly(True)
        entranceBox.setFixedHeight(32)
        font = getFont('box')
        entranceBox.setText(self.entrance)
        entranceBox.setFont(font)

        return entranceLabel, entranceBox


    def createExitingRegionLabels(self):
        # Label should be "To" + entranceTo.
        # Box should be leads to region
        if self.isSpawn or self.isOwl:
            exitLabelText = self.entranceFrom
        elif self.isWarpSong:
            warpSong = self.entranceFrom.split()
            warpSong = ' '.join(warpSong[:3])
            exitLabelText = warpSong
        else:
            exitLabelText = 'To ' + self.entranceTo

        exitLabel = QLabel(exitLabelText)
        exitLabel.setMinimumHeight(32)
        font = getFont('label')
        exitLabel.setFont(font)

        if self.isInterior:
            exitBoxText = self.leadsToRegion
        else:
            exitBoxText = self.leadsFromRegion + ' -> ' + self.leadsToRegion

        exitBox = QLineEdit()
        exitBox.setReadOnly(True)
        exitBox.setFixedHeight(32)
        font = getFont('box')
        exitBox.setText(exitBoxText)
        exitBox.setFont(font)

        return exitLabel, exitBox