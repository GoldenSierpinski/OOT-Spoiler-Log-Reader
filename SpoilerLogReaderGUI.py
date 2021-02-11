import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QPushButton, QFormLayout, QLabel, QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from SpoilerData import *
from Fonts import getFont

class SpoilerReaderGUI(QMainWindow):
    def __init__(self):
        super(SpoilerReaderGUI,self).__init__()
        self.filename = self.loadSpoilerData()
        self.spoilerData = SpoilerData(self.filename)

        # Set the window properties
        self.setWindowTitle('OoTR Spoiler Log Reader')
        self.setWindowIcon(QIcon('assets/Ocarina of Time.png'))
        self.setMinimumWidth(1600)

        # Create the central widget
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)

        # Create the general layout. This is a VBox, with file dialog, browse button, and hash on top,
        # and the item view on the bottom
        self.generalLayout = QVBoxLayout()
        self._centralWidget.setLayout(self.generalLayout)

        # Create the file dialog on the top of the general layout
        # self._createFileDialogLayout()
        self.createTopMatter()

        # Now create an HBox to act as the "overall" item view. Sections will include WOTH items,
        # dungeons and songs, and a tabbed item/entrance viewer
        self.itemLayout = QHBoxLayout()
        self.generalLayout.addLayout(self.itemLayout)

        # Create the scroll area for the WOTH items
        self.wothScroll = self.createScrollArea()
        wothLayout = QFormLayout()
        if self.spoilerData.isTriforceHunt:
            wothHeader = self.createHeaderLabel('Path of Gold')
        else:
            wothHeader = self.createHeaderLabel('Way of the Hero')
        wothLayout.addRow(wothHeader)
        for location in self.spoilerData.locations.values():
            if location.isWOTH:
                itemLabel,locationBox = location.createGUIElements()
                wothLayout.addRow(itemLabel,locationBox)
        wothWidget = QWidget()
        wothWidget.setLayout(wothLayout)
        self.wothScroll.setWidget(wothWidget)

        # Create the scroll area for the dungeons and songs
        self.dungeonsAndSongsScroll = self.createScrollArea()
        dungeonAndSongsLayout = QFormLayout()
        dungeonHeader = self.createHeaderLabel('Dungeons')
        dungeonAndSongsLayout.addRow(dungeonHeader)
        for locationList in self.spoilerData.tabs['Dungeon Prizes'].values():
            for location in locationList:
                itemLabel = location.item.createItemLabel()
                regionBox = location.region.createRegionBox()
                dungeonAndSongsLayout.addRow(itemLabel,regionBox)
        if self.spoilerData.isMQDungeons:
            for region in self.spoilerData.regions.values():
                if region.dungeonType == 'Minor':
                    itemLabel = self.spoilerData.items[region.name].createItemLabel()
                    regionBox = region.createRegionBox()
                    dungeonAndSongsLayout.addRow(itemLabel, regionBox)

        songHeader = self.createHeaderLabel('Songs')
        dungeonAndSongsLayout.addRow(songHeader)
        for locationList in self.spoilerData.tabs['Songs'].values():
            for location in locationList:
                itemLabel,locationBox = location.createGUIElements()
                dungeonAndSongsLayout.addRow(itemLabel, locationBox)
        dungeonsAndSongsWidget = QWidget()
        dungeonsAndSongsWidget.setLayout(dungeonAndSongsLayout)
        self.dungeonsAndSongsScroll.setWidget(dungeonsAndSongsWidget)

        # Create the tab widget and tabs
        self.tabWidget = QTabWidget()
        for tab in self.spoilerData.tabs:
            isTab = tabDictionary[tab]['isTab']
            byRegion = tabDictionary[tab]['byRegion']
            if isTab:
                if tab == 'Dungeon Items':
                    tabScroll = self.createDungeonItemsTab()
                else:
                    tabScroll = self.createGenericTab(tab,byRegion)
                if tabScroll is not None:
                    self.tabWidget.addTab(tabScroll,tab)

        # Check for shopsanity to add shops tab
        if self.spoilerData.isShopsanity:
            self.createShopsTab()

        # Check for entrance randomizer to add entrances and exits
        if self.spoilerData.isEntranceRandomzier:
            self.createEntrancesTab()

        # Add all of the widgets to the layout
        self.itemLayout.addWidget(self.dungeonsAndSongsScroll,2)
        self.itemLayout.addWidget(self.wothScroll,2)
        self.itemLayout.addWidget(self.tabWidget,3)

    def createGenericTab(self,tab,byRegion):
        tabItems = tabDictionary[tab]['items']
        tabLayout = QFormLayout()
        isEmpty = True
        if byRegion:
            regions = self.spoilerData.regions
            alphaRegions = list(regions.keys())
            alphaRegions.sort()
            for regionKey in alphaRegions:
                region = regions[regionKey]
                isEmptyRegion = True
                for location in region.locations:
                    item = location.item
                    if item.name in tabItems:
                        isEmpty = False
                        if isEmptyRegion:
                            regionHeader = self.createHeaderLabel(region.name)
                            tabLayout.addRow(regionHeader)
                            isEmptyRegion = False
                        itemLabel, locationBox = location.createGUIElements()
                        tabLayout.addRow(itemLabel,locationBox)
        else:
            for locationList in self.spoilerData.tabs[tab].values():
                for location in locationList:
                    isEmpty = False
                    itemLabel, locationBox = location.createGUIElements()
                    tabLayout.addRow(itemLabel, locationBox)

        if isEmpty:
            tabScroll = None
        else:
            tabWidget = QWidget()
            tabWidget.setLayout(tabLayout)
            tabScroll = self.createScrollArea()
            tabScroll.setWidget(tabWidget)

        return tabScroll

    def createDungeonItemsTab(self):
        dungeonItemsLayout = QFormLayout()
        dungeonItemList = self.spoilerData.dungeonItems
        isEmpty = True
        for dungeon in dungeonItemList:
            isRegionEmpty = True
            for location in dungeonItemList[dungeon]:
                isEmpty = False
                if isRegionEmpty:
                    dungeonHeader = self.createHeaderLabel(dungeon)
                    dungeonItemsLayout.addRow(dungeonHeader)
                    isRegionEmpty = False
                itemLabel, locationBox = location.createGUIElements()
                dungeonItemsLayout.addRow(itemLabel,locationBox)

        if isEmpty:
            dungeonItemScroll = None
        else:
            dungeonItemWidget = QWidget()
            dungeonItemWidget.setLayout(dungeonItemsLayout)
            dungeonItemScroll = self.createScrollArea()
            dungeonItemScroll.setWidget(dungeonItemWidget)
        return dungeonItemScroll

    def createShopsTab(self):
        shopLayout = QHBoxLayout()
        shops = self.spoilerData.shops
        for idx, shop in enumerate(shops):
            if not idx % 4:
                curColumn = QFormLayout()
                shopLayout.addLayout(curColumn)
            shopHeader = self.createHeaderLabel(shop)
            curColumn.addRow(shopHeader)
            for location in shops[shop]:
                itemBox = location.createItemBox()
                curColumn.addRow(itemBox)

        shopWidget = QWidget()
        shopWidget.setLayout(shopLayout)
        shopScroll = self.createScrollArea()
        shopScroll.setWidget(shopWidget)
        self.tabWidget.addTab(shopScroll,"Shops")

    def createEntrancesTab(self):
        entrancesLayout = QFormLayout()
        exitsLayout = QFormLayout()
        warpsLayout = QFormLayout()

        regions = self.spoilerData.regions
        entrances = self.spoilerData.entrances

        # Create warps section (Spawns, warp songs, and owls)
        warpsTabEmpty = True
        isEmpty = True

        # Spawns
        for entrance in entrances.values():
            if entrance.isSpawn:
                if isEmpty:
                    spawnsHeader = self.createHeaderLabel('Spawns')
                    warpsLayout.addRow(spawnsHeader)
                    isEmpty = False
                    warpsTabEmpty = False
                warpsLabel, warpsBox = entrance.createExitingRegionLabels()
                warpsLayout.addRow(warpsLabel, warpsBox)
        # Warps
        isEmpty = True
        warpSongs = {'Minuet of Forest Warp': [],
                     'Bolero of Fire Warp': [],
                     'Serenade of Water Warp': [],
                     'Nocturne of Shadow Warp': [],
                     'Requiem of Spirit Warp': [],
                     'Prelude of Light Warp': [],}
        for entrance in entrances.values():
            if entrance.isWarpSong:
                if isEmpty:
                    spawnsHeader = self.createHeaderLabel('Warp Songs')
                    warpsLayout.addRow(spawnsHeader)
                    isEmpty = False
                    warpsTabEmpty = False
                warpsLabel, warpsBox = entrance.createExitingRegionLabels()
                warpSongs[entrance.entranceFrom] = (warpsLabel,warpsBox)

        if not isEmpty:
            for warp in warpSongs.values():
                warpsLayout.addRow(warp[0], warp[1])

        # Owls
        isEmpty = True
        for entrance in entrances.values():
            if entrance.isOwl:
                if isEmpty:
                    spawnsHeader = self.createHeaderLabel('Owl Drops')
                    warpsLayout.addRow(spawnsHeader)
                    isEmpty = False
                    warpsTabEmpty = False
                warpsLabel, warpsBox = entrance.createExitingRegionLabels()
                warpsLayout.addRow(warpsLabel, warpsBox)

        if not warpsTabEmpty:
            warpsWidget = QWidget()
            warpsWidget.setLayout(warpsLayout)
            warpsScroll = self.createScrollArea()
            warpsScroll.setWidget(warpsWidget)
            self.tabWidget.addTab(warpsScroll,'Warps')

        # Create dungeon entrances section
        entrancesTabEmpty = True
        exitsTabEmpty = True
        isEmpty = True
        for region in regions.values():
            if region.isDungeon:
                for entrance in region.entrances:
                    if isEmpty:
                        dungeonHeader = self.createHeaderLabel('Dungeons')
                        entrancesLayout.addRow(dungeonHeader)
                        isEmpty = False
                        entrancesTabEmpty = False
                    entrancesLabel, entrancesBox = entrance.createEnteringRegionLabels()
                    entrancesLayout.addRow(entrancesLabel,entrancesBox)

        # Create entrances for remaining regions
        alphaRegions = list(regions.keys())
        alphaRegions.sort()
        for regionKey in alphaRegions:
            region = regions[regionKey]
            noEntrances = True
            noExits = True
            if not region.isDungeon:
                for entrance in region.entrances:
                    if entrance.isSpawn:
                        continue
                    if noEntrances:
                        regionHeader = self.createHeaderLabel(region.name)
                        entrancesLayout.addRow(regionHeader)
                        noEntrances = False
                        entrancesTabEmpty = False
                    entrancesLabel,entrancesBox = entrance.createEnteringRegionLabels()
                    entrancesLayout.addRow(entrancesLabel,entrancesBox)
                for exits in region.exits:
                    if noExits:
                        regionHeader = self.createHeaderLabel(region.name)
                        exitsLayout.addRow(regionHeader)
                        noExits = False
                        exitsTabEmpty = False
                    exitsLabel, exitsBox = exits.createExitingRegionLabels()
                    exitsLayout.addRow(exitsLabel,exitsBox)

        if not entrancesTabEmpty:
            entrancesWidget = QWidget()
            entrancesWidget.setLayout(entrancesLayout)
            entrancesScroll = self.createScrollArea()
            entrancesScroll.setWidget(entrancesWidget)
            self.tabWidget.addTab(entrancesScroll,'Entrances')

        if not exitsTabEmpty:
            exitsWidget = QWidget()
            exitsWidget.setLayout(exitsLayout)
            exitsScroll = self.createScrollArea()
            exitsScroll.setWidget(exitsWidget)
            self.tabWidget.addTab(exitsScroll, 'Exits')

    def createTopMatter(self):
        topMatterLayout = QHBoxLayout()

        # Create Version Display
        versionLayout = QFormLayout()
        versionLabel = self.createHeaderLabel('Version')
        version = self.spoilerData.version
        versionBox = QLineEdit()
        versionBox.setReadOnly(True)
        versionBox.setFixedHeight(32)
        versionBox.setFont(getFont('box'))
        versionBox.setText(version)
        versionLayout.addRow(versionLabel,versionBox)
        versionWidget = QWidget()
        versionWidget.setFixedWidth(500)
        versionWidget.setLayout(versionLayout)

        # Create Settings String
        settingsLayout = QFormLayout()
        settingsLabel = self.createHeaderLabel('Setting String')
        settingString = self.spoilerData.settingsString
        settingsBox = QLineEdit()
        settingsBox.setReadOnly(True)
        settingsBox.setFixedHeight(32)
        settingsBox.setFont(getFont('box'))
        settingsBox.setText(settingString)
        settingsLayout.addRow(settingsLabel,settingsBox)
        settingsWidget = QWidget()
        settingsWidget.setLayout(settingsLayout)

        # Create Seed Hash display
        hashOptions = {
            'Deku Stick':               'Deku Stick',
            'Deku Nut':                 'Deku Nut',
            'Bombchu':                  'Bombchus',
            'Longshot':                 'Longshot',
            'Beans':                    'Magic Bean Pack',
            'Bottled Fish':             'Bottle with Fish',
            'Bottled Milk':             'Bottle with Milk',
            'Cucco':                    'Pocket Cucco',
            'Mushroom':                 'Odd Mushroom',
            'Saw':                      'Poachers Saw',
            'Frog':                     'Eyeball Frog',
            'Skull Token':              'Gold Skulltula Token'}

        hashLayout = QHBoxLayout()
        seedHash = self.spoilerData.hash
        hashLabel = self.createHeaderLabel('Hash: ')
        hashLayout.addWidget(hashLabel)
        for icon in seedHash:
            if icon in self.spoilerData.items:
                item = icon
            else:
                item = hashOptions[icon]
            iconLabel = self.spoilerData.items[item].createItemLabel()
            hashLayout.addWidget(iconLabel)
        hashWidget = QWidget()
        hashWidget.setLayout(hashLayout)
        hashWidget.setFixedWidth(275)

        topMatterLayout.addWidget(versionWidget)
        topMatterLayout.addWidget(settingsWidget)
        topMatterLayout.addWidget(hashWidget)

        self.generalLayout.addLayout(topMatterLayout)

    def _createFileDialogLayout(self):
        # Create file dialog layout
        fileDialog = QHBoxLayout()

        # Create file name box
        self.fileNameBox = QLineEdit()
        self.fileNameBox.setAlignment(Qt.AlignLeft)
        self.fileNameBox.setReadOnly(True)

        # create browse button
        self.browseButton = QPushButton('Browse...')

        # Add dialog box and browse button to dialog layout
        fileDialog.addWidget(self.fileNameBox)
        fileDialog.addWidget(self.browseButton)

        # Add dialog layout to main window
        self.generalLayout.addLayout(fileDialog)

    # Opens a file dialog window and prompts the user for a JSON file
    def loadSpoilerData(self):
        # Ask the user to select a file
        fileName = QFileDialog.getOpenFileName(self, "Select Spoiler Log", "", "JSON Files (*.json)")
        fileName = fileName[0]
        return fileName

    @staticmethod
    def createScrollArea():
        widget = QScrollArea()
        widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        widget.setWidgetResizable(True)
        return widget

    @staticmethod
    def createHeaderLabel(text):
        label = QLabel(text)
        label.setFont(getFont('header'))
        label.setAlignment(Qt.AlignCenter)
        return label

def main():
    """Main Function"""
    # Create an instance of QApplication
    mainWindow = QApplication(sys.argv)
    # Render the GUI
    view = SpoilerReaderGUI()
    view.showMaximized()

    # Execute GUI main loop
    sys.exit(mainWindow.exec())

if __name__ == '__main__':
    main()