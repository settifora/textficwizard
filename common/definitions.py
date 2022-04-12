import re

URGENCY_MESSAGE = 0
URGENCY_ALERT = 1
URGENCY_WARN = 2

OUTPUT_DIR = 'output'
CSS_FILE_NAME = 'style.css'

HEX_COLOR_REGEX = re.compile('^#[0-9A-Fa-f]{3}|#[0-9A-Fa-f]{6}$')

CSS_CHARACTER_CLASSES = """
.CHARACTER_NAME .message
{
  background: CHARACTER_COLOR;
  color: CHARACTER_FONT;
}

.CHARACTER_NAME .bottom-text::after
{
  border-right: 0.5em solid CHARACTER_COLOR;
}

.group-leader.CHARACTER_NAME .bottom-text::after
{
  border-left: 0.5em solid CHARACTER_COLOR;
}
"""
    
BASE_CSS_CLASSES = """
.hide
{
  display: none;
}

.message-block
{
  display: grid;
  width:97%;
  margin: auto;
}

.messages-header
{
  font-weight: bold;
  margin-top: 1em;
  padding: 5px;
  text-align: center;
  background: #f6f6f6;
  border-bottom: 1px solid #b2b2b2;
  color: #000;
}

.sender-block span
{
    float: left;
}

.group-leader span
{
    float: right;
}

.name-tag
{
    font-weight: bold;
    color: #7b7c80;
    font-size: .75em;
    padding: 0;
    margin: 1em 1.25em 0.25em 1.75em;
    clear: both;
}

.message-action {
    margin: 1.25em auto 0.75em auto;
    font-weight: bold;
    padding: 0;
    font-style: italic;
    color: #7b7c80;
    clear: both;
}

.message
{
    color: #000;
    background-color: #e0e0e8;
    margin: 0 0.75em 0.1em;
    border-radius: 1.25em;
    padding: 0.5em 1em;
    max-width: 75%;
    width: fit-content;
    clear: both;
    position: relative;
    line-height: 1.5;
}

.bottom-text::after {
    content: "";
    position: absolute;
    left: -0.5em;
    bottom: 0;
    width: 0.5em;
    height: 1em;
    border-bottom-right-radius: 1em 0.5em;
    border-right: 0.5em solid #e0e0e8;
}

.group-leader .bottom-text::after {
    content: "";
    position: absolute;
    right: -0.5em;
    left: unset;
    bottom: 0;
    width: 0.5em;
    height: 1em;
    border-bottom-right-radius: 0.5em;
    border-right: none !important;
    border-bottom-left-radius: 1em 0.5em;
    border-left: 0.5em solid #e0e0e8;
}

.delimiter-bar
{
    border: 1px solid black;
    width: 33%;
    margin: 2em auto;
}
"""

PREVIEW_CSS_CLASSES = """
:root
{
    font-family: 'Lucida Grande','Lucida Sans Unicode','GNU Unifont',Verdana,Helvetica,sans-serif;
    max-width: 72em;
    font-size: 100%;
    margin: auto;
}
"""

def getContrastColor(color):
    try:
        red = int(color[1:3], 16)
        green = int(color[3:5], 16)
        blue = int(color[5:7], 16)
        
        if (red*0.299 + green*0.587 + blue*0.114) > 150:
            fontColor = '#000000'
        else:
            fontColor = '#ffffff'
    
    except ValueError:
        fontColor = '#000000'
        
    return fontColor