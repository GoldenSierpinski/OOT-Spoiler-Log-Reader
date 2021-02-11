from PyQt5.QtGui import QFont

def getFont(fontName):
    font = QFont()
    if fontName.lower() == 'header':
        font.setFamily('Arial')
        font.setPointSize(16)
        font.setBold(True)
    elif fontName.lower() == 'label':
        font.setPointSize(12)
    elif fontName.lower() == 'box':
        font.setPointSize(12)
        font.setFamily('Consolas')
    elif fontName.lower() == 'italic':
        font.setPointSize(12)
        font.setItalic(True)

    return font