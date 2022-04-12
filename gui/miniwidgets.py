from PySide2.QtCore import Qt
from PySide2.QtGui import QCursor, QColor, QIcon
from PySide2.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout, QColorDialog

from common.definitions import getContrastColor, HEX_COLOR_REGEX
from common import resources

# Class representing a composite widget used for picking/ entering hex colors
class ColorPickerEntry(QWidget):
    # Constructor
    # Parameters:
    #     parent: The parent widget
    def __init__(self, parent):
        # Call superconstructor to initialise the widget
        super().__init__(parent)
        
        # Create the sub-widgets
        self.colorEntryBox = QLineEdit()
        self.colorPickerButton = QPushButton('', parent)
        self.colorPickerButton.setIcon(QIcon(':/icons/dropper.png'))
        
        # Handle color picker button clicks
        self.colorPickerButton.clicked.connect(self.setColor)
        
        # Handle changes to the text entry contents
        self.colorEntryBox.textChanged.connect(self.colorChanged)
        
        # Lay out the widget
        hBoxLayout = QHBoxLayout()
        hBoxLayout.setContentsMargins(0,0,0,0)
        hBoxLayout.addWidget(self.colorEntryBox)
        hBoxLayout.addWidget(self.colorPickerButton)
        self.setLayout(hBoxLayout)
    
    # Method: Handle color picker button clicks.
    def setColor(self): 
        #  Open a color picker dialog and get the selected color
        color = QColorDialog.getColor(initial=QColor(self.colorEntryBox.text()))
        
        # Write the selected color's (hexadecimal) name into the text entry
        self.colorEntryBox.setText(color.name())
    
    # Method: Handle changes to the text entry contents.
    def colorChanged(self):
        color = None
        fontColor = None
        
        # Get the new content of the text entry
        colorText = self.colorEntryBox.text()
        
        if not colorText:
            # The box is empty; reset its style
            color = colorText = 'white'
            fontColor = 'black'
        elif HEX_COLOR_REGEX.fullmatch(colorText):
            # The box contains a valid hex color. Set the background to that
            # color, and the font color to an appropriate contrasting color
            # (either black or white).
            color = colorText
            fontColor = getContrastColor(color)
        
        # Style the text entry box
        if color:
            self.colorEntryBox.setStyleSheet('QLineEdit { background: ' + color + '; color: ' + fontColor + ' } ')
    
    # Method: Set the widget's text (just write it into the text entry)
    def setText(self, text):
        self.colorEntryBox.setText(text)
    
    # Method: Get the widget's text (from the text entry)
    # Returns: str
    def text(self):
        return self.colorEntryBox.text()
        
# Class representing a clickable button in the GUI
class ClickyButton(QPushButton):
    # Constructor
    # Parameters:
    #     text:       The display text for the button
    #     parent:     The parent widget for the button
    #     className:  The class name to set on the widget (optional)
    def __init__(self, text, parent, className=None):
        # Call superconstructor to initialise the widget
        super().__init__(text, parent)
        
        # Set the cursor to the pointing hand
        buttonCursor = QCursor(Qt.PointingHandCursor)
        self.setCursor(buttonCursor)
        
        # If a class was specified, set it on the button
        if className:
            self.setProperty('class', className)