from PyQt5.QtWidgets import QLineEdit
from Fonts import getFont
from Item import Item

class Location:
    def __init__(self,name):
        self.name = name
        self.display = None
        self.item = None
        self.price = None
        self.model = None
        self.region = []
        self.isWOTH = False
        self.isDungeon = False

        if "Shop" in self.name or "Bazaar" in self.name:
            self.isShop = True
            self.color = "background-color: #ADADFF"
        else:
            self.isShop = False
            if "GS" in self.name:
                self.color = "background-color: #FFFFAD;"
            elif "Cow" in self.name:
                self.color = "background-color: #FFADAD;"
            elif "Deku Scrub" in self.name:
                self.color = "background-color: #ADFFAD;"
            else:
                self.color = "background-color: #FFFFFF"

    def addItem(self, item, itemObj=None):
        if itemObj is not None:
            self.item = itemObj
        else:
            self.item = Item(item)

        self.item.location.append(self)

        if 'price' in item:
            self.price = item['price']
        if 'model' in item:
            self.model = item['model']
    def setDisplay(self):
        price = ''
        model = ''
        if self.price is not None:
            price = '[' + str(self.price) + '] '

        if self.model is not None:
            model = ' [' + str(self.model) + ']'

        self.display = price + self.name + model

    def createGUIElements(self):
        itemLabel = self.item.createItemLabel()
        locationBox = self.createLocationBox()
        return itemLabel, locationBox

    def createLocationBox(self):
        locationBox = QLineEdit()
        locationBox.setReadOnly(True)
        locationBox.setFixedHeight(32)
        locationBox.setStyleSheet(self.color)
        font = getFont('box')
        if self.isWOTH:
            font.setBold(True)
        locationBox.setFont(font)

        if self.display is None:
            self.setDisplay()

        locationBox.setText(self.display)

        return locationBox

    # For shops tab
    def createItemBox(self):
        item = self.item
        price = self.price

        itemBox = QLineEdit()
        itemBox.setReadOnly(True)
        itemBox.setFixedHeight(32)
        font = getFont('box')
        if "Buy" in item.name:
            font = getFont('italic')
            itemBox.setStyleSheet("background-color: #ADADAD;")
        elif price > 500:
            itemBox.setStyleSheet("background-color: #FFADFF;")
        elif price > 200:
            itemBox.setStyleSheet("background-color: #FFADAD;")
        elif price > 99:
            itemBox.setStyleSheet("background-color: #ADADFF;")
        else:
            itemBox.setStyleSheet("background-color: #ADFFAD;")
        itemBox.setText('[' + str(price) + '] ' + item.name)
        itemBox.setFont(font)
        return itemBox

