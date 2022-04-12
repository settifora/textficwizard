from PySide2.QtWidgets import QMainWindow
from PySide2.QtWebEngineWidgets import QWebEngineView

# Class representing the pop-up window used to preview output files
from common.definitions import PREVIEW_CSS_CLASSES
from config.manager import generateCss

class FilePreviewWindow(QMainWindow):
    # Constructor
    # Parameters: 
    #     filename: The name (path) of the file to preview
    #     parent: The parent application window (instance of AppMainWindow)
    def __init__(self, filename, parent):
        # Call superconstructor to initialise the widget
        super().__init__(parent)

        # Regenerate the stylesheet to make sure it matches current config
        generateCss()
        
        # Load the generated stylesheet and append the extra classes that the
        # preview window will need
        with open('output/style.css', 'r') as cssFile:
            css = cssFile.read() + PREVIEW_CSS_CLASSES

        # Load the HTML file that's being previewed
        with open(filename, 'r') as htmlFile:
            html = htmlFile.read()

        # Add a <head> tag containing the CSS style to the HTML. We need to do
        # this here because the output files don't reference the stylesheet
        # (since it will be set as a work skin), and in any case the 
        # QWebEngineView widget refuses to load an external stylesheet.
        html = '<!DOCTYPE html><head><style>' + css + '</style></head>' + html

        # Get the QWebEngineView widget and give it the HTML
        webView = QWebEngineView()
        webView.setHtml(html)
        
        # Put the QWebEngineView widget into the file preview window
        self.setCentralWidget(webView)
        
        # Name the window and put it in a nice position
        self.setWindowTitle('TextFic Wizard File Preview')
        self.setGeometry(parent.geometry().adjusted(150, 100, 150, 100))
        
        # Show the window
        self.showMaximized()