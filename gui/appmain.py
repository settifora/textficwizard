import sys
from math import floor
from functools import partial
import os
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon

from common.definitions import *
from common import resources
from config.manager import getConfigManager
from converter.ficfileconverter import processFile
from gui.filepreview import FilePreviewWindow
from gui.miniwidgets import *
from gui.styles import getAppStyleSheet, getCharacterButtonStyle, URGENCY_COLORS

# Class representing the List Characters sub-panel
class ListCharactersPanel(QWidget):
    def __init__(self, mainWindow):
        super().__init__(mainWindow)
    
        characterButtons = []
    
        # Create a button for each configured character
        for character in getConfigManager().listCharacters():
            characterButton = ClickyButton(character.getDisplayName(),
                                           self)
            characterButton.setStyleSheet(getCharacterButtonStyle(character))
            characterButton.clicked.connect(partial(mainWindow.addEditCharacter, character))
            
            characterButtons.append(characterButton)
        
        # Create a button to add a new character       
        addButton = ClickyButton('Add Character', self, 'content-action-button')
        addButton.clicked.connect(mainWindow.addEditCharacter)
        
        # Do layout for the panel
        layout = QGridLayout()
        self.setLayout(layout)
      
        # Add character buttons
        index = 0
        for characterButton in characterButtons:
            layout.addWidget(characterButton, floor(index/5), index % 5)
            index += 1
        
        # If we don't have at least one full row of buttons, add empty widgets
        # to maintain the layout
        if index < 5:
            for ii in range(index, 5):
                layout.addWidget(QWidget(), 0, ii)
                   
        # Finally, the Add button, with a spacer to keep it at the bottom
        layout.addItem(QSpacerItem(1, 
                                   1, 
                                   QSizePolicy.Minimum, 
                                   QSizePolicy.Expanding),
                       floor(index/5)+1, 
                       4)
        layout.addWidget(addButton, floor(index/5)+2, 1, 1, 3)

# Class representing the Add/ Edit Character sub-panel
class AddEditCharacterPanel(QWidget):
    # Constructor
    # Parameters:
    #     mainWindow:  The parent application window
    #     character:   The character being edited (if any)
    def __init__(self, mainWindow, character=None):
        # Call superconstructor to initialise the widget
        super().__init__(mainWindow)
        
        # Store the parent application window for later
        self.mainWindow = mainWindow      
                      
        # Create input boxes for the character's name and bubble color
        self.nameEntryBox = QLineEdit()       
        self.colorEntryBox = ColorPickerEntry(self)
        
        # Create save button
        saveButton = ClickyButton('Save', self, 'content-action-button')
        saveButton.clicked.connect(self.saveCharacter)
        
        # Create a delete button if needed
        if character:
            deleteButton = ClickyButton('Delete', self, 'content-action-button')
            deleteButton.clicked.connect(self.deleteCharacter)
        
        # If we're editing a character, pre-load its details into the form
        if character:
            self.nameEntryBox.setText(character.getDisplayName())
            self.colorEntryBox.setText(character.color)
        
        # Set up the widget layout
        vBoxWidget = QWidget()
        vBoxLayout = QVBoxLayout()
        vBoxLayout.setSpacing(0)
        vBoxWidget.setLayout(vBoxLayout)
        
        # Add widgets vertically
        vBoxLayout.addStretch(1)
        vBoxLayout.addWidget(self.nameEntryBox)
        vBoxLayout.addWidget(self.colorEntryBox)
        vBoxLayout.addWidget(saveButton)
        
        # Only show the delete button if we're editing an existing character
        if character:
            vBoxLayout.addWidget(deleteButton)
        
        vBoxLayout.addStretch(1)
        
        # Add vertical widget panel to middle of this panel
        hBoxLayout = QHBoxLayout()
        hBoxLayout.addStretch(1)
        hBoxLayout.addWidget(vBoxWidget)
        hBoxLayout.addStretch(1)
        self.setLayout(hBoxLayout)
    
    # Method to save the character being configured
    def saveCharacter(self):
        # Try to add the character
        success = getConfigManager().addCharacter(self.nameEntryBox.text(),
                                             self.colorEntryBox.text())
        
        if success:
            # Show success message and return to character list
            self.mainWindow.sendMessage('Character saved successfully', URGENCY_ALERT)
            self.mainWindow.listCharacters(False)
        else:
            # Show an error - the config must be faulty
            self.mainWindow.sendMessage('ERROR: Character config invalid - please retry', URGENCY_WARN)
    
    # Method to delete the character being edited
    def deleteCharacter(self):
        # Try to delete the character
        success = getConfigManager().deleteCharacter(self.nameEntryBox.text())
        
        if success:
            # Show success message and return to character list
            self.mainWindow.sendMessage('Character deleted successfully', URGENCY_ALERT)
            self.mainWindow.listCharacters(False)
        else:
            # Show an error - the character must not exist (this is unexpected)
            self.mainWindow.sendMessage('ERROR: The specified character does not exist', URGENCY_WARN)
        
# Class representing the Preview Output sub-panel
class FilePreviewPanel(QWidget):
    # Constructor
    # Parameters:
    #     mainWindow:  The parent application window
    def __init__(self, mainWindow):
        # Call superconstructor to initialise the widget
        super().__init__(mainWindow)
        
        # Store the parent application window for later
        self.mainWindow = mainWindow
        
        # Create a select file button
        selectFileButton = ClickyButton('Select file to preview',
                                        self, 
                                        'content-action-button')
                                        
        selectFileButton.clicked.connect(self.getFileAndPreview)
        
        # Setup the layout of the panel
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addStretch(1)
        vBoxLayout.addWidget(selectFileButton)
        vBoxLayout.addStretch(2)
        self.setLayout(vBoxLayout)

    # Method to select a file and open the preview window
    def getFileAndPreview(self):
        # Use a file picker dialog to select the file to preview
        filename = QFileDialog.getOpenFileName(self, 
                                               'Open file', 
                                               'output', 
                                               'HTML files (*.html)')[0]
        
        if filename and os.path.isfile(filename):
            filePreviewWindow = FilePreviewWindow(filename, self.mainWindow)

# Class representing the Process Files sub-panel
class FileProcessPanel(QWidget):
    # Constructor
    # Parameters:
    #     mainWindow:  The parent application window
    def __init__(self, mainWindow):
        # Call superconstructor to initialise the widget
        super().__init__(mainWindow)
        
        # Store the parent application window for later
        self.mainWindow = mainWindow
        
        # Create a select files button
        selectFilesButton = ClickyButton('Select files to process',
                                         self,
                                         'content-action-button')

        selectFilesButton.clicked.connect(self.getFilesAndProcess)
        
        # Setup the layout of the panel
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addStretch(1)
        vBoxLayout.addWidget(selectFilesButton)
        vBoxLayout.addStretch(2)
        self.setLayout(vBoxLayout)
        
    # Method to get a list of input files and process them
    def getFilesAndProcess(self):
        # Get the input file list via a file picker dialog
        inputList = QFileDialog.getOpenFileNames(self, 
                                                 'Open file',
                                                 os.path.expanduser('~/Documents'),
                                                 'Documents (*.docx)')[0]
        
        # If ths list is empty, we're done here
        if not inputList:
            return
        
        resultMessages = []
        
        for filename in inputList:
            if (os.path.isfile(filename)):
                # Process the file
                result = processFile(filename)
                outfile = result[0]
                characters = result[1]
                
                # Assume success (ew, but currently failures crash the app, so...)
                # Build a label to report the (presumed) success. Include a 
                # hyperlink to preview the results.
                miniMessageLabel = QLabel(self)
                message = 'File processed successfully: ' + \
                          os.path.basename(filename) + \
                          ' (<a href="' + outfile + '">Preview</a>)'
                miniMessageLabel.setText(message)
                miniMessageLabel.linkActivated.connect(self.mainWindow.handlePreviewClick)
                resultMessages.append(miniMessageLabel)
                
                # Warn the user if there are any unknown characters
                if (characters):
                    knownCharacters = []
                    unknownCharacters = []
                    for character in characters:
                        if getConfigManager().getCharacter(character):
                            knownCharacters.append(character)
                        else:
                            unknownCharacters.append(character)
                    
                    if unknownCharacters:
                        # Build a message label - indent it so that it's 
                        # obvious which file it pertains to.
                        charactersLabel = QLabel(self)
                        charactersLabel.setWordWrap(True)
                        message = 'File contained unknown characters: ' + \
                                  ', '.join(unknownCharacters)
                        charactersLabel.setText(message)
                        charactersLabel.setProperty('class', 'indent')
                        resultMessages.append(charactersLabel)
        
        # Display the results
        self.mainWindow.displayResults(True, resultMessages)  

# Class representing the results sub-panel after a Process Files operation
class DisplayResultsPanel(QWidget):
    def __init__(self, mainWindow, resultMessages):
        # Call superconstructor to initialise the widget
        super().__init__()
        
        # Setup the layout of the panel
        vBoxLayout = QVBoxLayout()
        self.setLayout(vBoxLayout)
    
        # Add the results to the layout
        for resultMessage in resultMessages:
            self.layout().addWidget(resultMessage)
        self.layout().addStretch(1)           

# Class representing the main window of the app
class AppMainWindow(QMainWindow):
    # Constructor
    def __init__(self):
        # Call superconstructor to initialise the widget
        super().__init__()

        # Set the window properties nicely. Use 0 for the width and height - 
        # it'll resize automatically when we add stuff.
        self.setWindowTitle('TextFic Wizard')
        self.setWindowIcon(QIcon(':/icons/app-icon.png'))
        self.setStyleSheet(getAppStyleSheet())
        self.setGeometry(200, 200, 0, 0)
        
        # Top message bar items
        topBar = QWidget()
        topBar.setProperty('class', 'top-bar')
        
        self.messageBarLabel = QLabel(topBar)
        
        # Side menu bar items
        sideBar = QWidget()
        sideBar.setProperty('class', 'side-bar')
                
        manageCharacterButton = ClickyButton('Manage Characters', sideBar, 'action-button')
        manageCharacterButton.clicked.connect(self.listCharacters)
                
        processFileButton = ClickyButton('Process Files', sideBar, 'action-button')
        processFileButton.clicked.connect(self.processFiles)
        
        previewFileButton = ClickyButton('Preview Output', sideBar, 'action-button')
        previewFileButton.clicked.connect(self.previewOutput)
        
        exitButton = ClickyButton('EXIT', sideBar, 'exit-button')
        exitButton.clicked.connect(sys.exit)
        
        # Content panel items
        contentPanel = QWidget()
        contentPanel.setProperty('class', 'content-panel')
                
        # Layout for the top bar
        messageBarLayout = QHBoxLayout()
        messageBarLayout.addWidget(self.messageBarLabel)
        topBar.setLayout(messageBarLayout)
        
        # Layout for the sidebar
        sideBarLayout = QVBoxLayout()
        sideBarLayout.addWidget(manageCharacterButton)
        sideBarLayout.addWidget(processFileButton)
        sideBarLayout.addWidget(previewFileButton)
        sideBarLayout.addStretch(1)
        sideBarLayout.addWidget(exitButton)
        sideBar.setLayout(sideBarLayout)
        
        # Content panel (blank for now, but used later)
        self.contentPanel = QWidget()
                
        # Layout for the whole window
        self.mainLayout = QGridLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setRowStretch(1, 1)
        self.mainLayout.setColumnStretch(1, 1)
        
        self.mainLayout.addWidget(topBar, 0, 0, 1, 2)
        self.mainLayout.addWidget(sideBar, 1, 0)
        self.mainLayout.addWidget(contentPanel, 1, 1)
        
        mainPanel = QWidget()
        mainPanel.setLayout(self.mainLayout)
        
        self.setCentralWidget(mainPanel)
        
        # Reposition the window to the middle of the screen
        self.adjustSize()
        xPos = round(0.5 * (QDesktopWidget().availableGeometry().width() - self.geometry().width()))
        yPos = round(0.5 * (QDesktopWidget().availableGeometry().height() - self.geometry().height()))
        self.move(xPos, yPos)
    
    # Method to display a message in the top bar
    # Parameters:
    #     line:     The message to display
    #     urgency:  The urgency of the message
    def sendMessage(self, line, urgency):
        # Urgency can't be more than the highest level defined
        urgency = min(urgency, len(URGENCY_COLORS) - 1)

        # Display the message - with inline HTML color formatting
        startHtml  = '<font color="SETCOLOR">';
        endHtml    = '</font>';
        startHtml = startHtml.replace('SETCOLOR', URGENCY_COLORS[urgency])
        line = startHtml + line + endHtml
        self.messageBarLabel.setText(line)
    
    # Method to clear the top bar message
    def clearMessage(self):
        self.sendMessage('', 0)

    # Method to replace the content panel with a new widget
    def setContentPanel(self, widget):
        if self.contentPanel:
            self.mainLayout.removeWidget(self.contentPanel)
            self.contentPanel.deleteLater()
        self.contentPanel = widget
        self.mainLayout.addWidget(widget, 1, 1)
        self.contentPanel.setProperty('class', 'content-panel')

    # Method used by action button: display process files panel
    def processFiles(self):
        self.clearMessage()
        self.setContentPanel(FileProcessPanel(self))
    
    # Method to display results of a process files operation
    def displayResults(self, success, resultMessages):
        if success:
            self.sendMessage('Files processed successfully', URGENCY_ALERT)
        
        self.setContentPanel(DisplayResultsPanel(self, resultMessages))
    
    # Method to handle a click on one of the 'preview' links in the results
    def handlePreviewClick(self, link):
        FilePreviewWindow(link, self)
    
    # Method used by action button: display preview output panel
    def previewOutput(self):
        self.clearMessage()     
        contentPanel = FilePreviewPanel(self)
        self.setContentPanel(contentPanel)
    
    # Method used by action button: display add/ edit character panel
    def addEditCharacter(self, character=None):
        self.clearMessage()
        contentPanel = AddEditCharacterPanel(self, character)
        self.setContentPanel(contentPanel)
    
    # Method used by action button: display list characters panel
    # Parameters:
    #     clearMessage:  Whether to clear the top message bar before displaying
    #                    the panel
    def listCharacters(self, clearMessage=True):
        if clearMessage:
            self.clearMessage()
        contentPanel = ListCharactersPanel(self)
        self.setContentPanel(contentPanel)   
