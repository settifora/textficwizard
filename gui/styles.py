from math import sqrt
import re

# Array of colors used in the app. 
# Broadly speaking:
#     0: Background of sidebar
#     1: Background of top bar, and buttons in content panel
#     2: Background of buttons in sidebar
#     3: Alert-level messages in top bar
#     4: Background of content-panel and most text on #s 0-2
APP_COLORS = ['#363845', '#22174F', '#CE5A12', '#f4ca16', '#F3F3F4']
URGENCY_COLORS = [APP_COLORS[4], APP_COLORS[3], 'red']

# Main QSS stylesheet for the app. This uses two kinds of variable string - 
# both handled by functions below, as CSS variables don't work:
#     '--APP_COLOR_[0-4]': The given app color, as defined in APP_COLORS
#     '--transform[+/-n]': Lighten (+) / darken (-) the given color by n shades
# Note that these can be combined, e.g. '--transform1:APP_COLOR_0'.
# See methods below for further details.
APP_STYLE_SHEET = """
QPushButton
{
    font-family: Helvetica, sans-serif;
    font-weight: bold;
}

QLabel
{
    font-family: Helvetica, sans-serif;
}

.top-bar 
{ 
    background: --APP_COLOR_1;
    min-height: 60px;
    max-height: 60px;
    min-width: 1000px;
}

.side-bar 
{ 
    background: --APP_COLOR_0;
    min-width: 310px;
    max-width: 310px;
    min-height: 500px;
    padding: 0px;
}

.top-bar QLabel
{
    font-size: 20px;
    color: --APP_COLOR_4;
    font-weight: bold;
    padding-left: 20px;
}

.side-bar QPushButton
{
    font-size: 18px;
    padding: 15px 3px;
    color: --APP_COLOR_4;
    background: --APP_COLOR_2;  
    border-radius: 20px;
    max-width: 250px;
    min-width: 250px;
}

.side-bar QPushButton:hover
{
    background: --transform1--APP_COLOR_2;
    padding: 12px 0px;
}

.action-button
{
    margin: 10px 20px 3px 20px;
}

.action-button:hover
{
    margin: 7px 17px 0px 17px;
}

.exit-button
{
    margin: 3px 20px 10px 20px;
}

.exit-button:hover
{
    margin: 0px 17px 7px 17px;
}

.content-panel
{ 
    background: --APP_COLOR_4;
    padding: 15px 10px;
}

.content-panel QLabel
{ 
    background: --transform-1--APP_COLOR_4;
    font-size: 12px;
    padding: 8px;
}

.content-panel QLineEdit
{ 
    font-size: 16px;
    padding: 8px;
    margin-bottom: 8px;
}

.content-action-button
{
    background: --APP_COLOR_1;
    color: --APP_COLOR_4;
    font-size: 16px;
    padding: 17px;
    margin: 10px 20px 3px 20px;
    font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
    border-radius: 22px;
    letter-spacing: 1px;
}

.content-action-button:hover
{
    background: --transform1--APP_COLOR_1;
    padding: 14px;
    margin: 7px 17px 0px 17px;
}

.indent
{ 
    margin-left: 30px;
}
"""

# Function to darken/ lighten a color by a certain amount
# Parameters:
#     color:   The color to modify.
#     amount:  The number of 'shades' to lighten (positive)/ darken (negative).
# Returns: str  The new color in hex format (e.g. '#000000')
def transformColor(color, amount):
    newColorParts = ['#']
    
    # Handle each of RGB parts separately.
    for ii in range(3):
        colorPart = int(color[1 + (2*ii) : 3 + (2*ii)], 16)
        
        # Do the transform and get the result as a hex string (without '0x').
        # Formula is my own hokey creation. Note that we don't allow the 
        # result to get outside the 0-255 range.
        increment = (amount * ((colorPart**2) + (255-colorPart)**2))/3000
        newColorPart = max(min(colorPart + increment, 255), 0)
        newColorHexPart = hex(round(newColorPart))[2:]
        
        # If we've ended up with a single-character string, prepend '0'
        if (len(newColorHexPart) < 2):
            newColorHexPart = "0" + newColorHexPart
        
        # Store this part of the color
        newColorParts.append(newColorHexPart)
   
    return ''.join(newColorParts)

# Function to replace all '--transform' color variables in a given stylesheet
# with an appropriately-transformed color value.
# Parameters:
#     styleSheet:  The stylesheet to modify.
# Returns: str  The new stylesheet
def transformColors(styleSheet):
    while True:
        match = re.search('(--transform([-]?[0-9])(#[0-9a-fA-F]{6}))', styleSheet)
        
        # No transform variables left - quit
        if not match:
            break
        
        # Transform the captured color by the captured amount
        newColor = transformColor(match.group(3), int(match.group(2)))
        
        # Replace the captured color variable with the new color
        styleSheet = styleSheet.replace(match.group(1), newColor) 
        
    return styleSheet

# Function to replace all --APP_COLOR variables in a given stylesheet with the
# appropriate color string from APP_COLORS.
# Parameters:
#     styleSheet:  The stylesheet to modify.
# Returns: str  The new stylesheet
def useAppColors(styleSheet):
    for ii in range(len(APP_COLORS)):
        styleSheet = styleSheet.replace("--APP_COLOR_" + str(ii), APP_COLORS[ii])
        
    return styleSheet

# Function to get the app stylesheet, replacing any variables as appropriate.
# Returns: str  The generated stylesheet
def getAppStyleSheet():
    styleSheet = APP_STYLE_SHEET
    
    styleSheet = useAppColors(styleSheet)    
    styleSheet = transformColors(styleSheet)
        
    return styleSheet

# Function to generate a button stylesheet for character-specific buttons in
# the 'list characters' view. Replaces variables as appropriate.
# Parameters:
#     character:  The Character object for which to generate the stylesheet.
# Returns: str  The generated stylesheet
def getCharacterButtonStyle(character):
    style = """
        QPushButton { 
            background: --BACKGROUND_COLOR;
            color: --FONT_COLOR;
            font-size: 16px;
            padding: 15px 0px;
            margin: 8px;
            font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
            border-radius: 22px;
            letter-spacing: 1px;
        }
        
        QPushButton:hover { 
            background: --transform1:--BACKGROUND_COLOR;
            padding: 18px 3px;
            border-radius: 25px;
            margin: 5px;
        }
    """
    
    style = style.replace('--BACKGROUND_COLOR', character.color)
    style = style.replace('--FONT_COLOR', character.fontColor)
    style = useAppColors(style)
    style = transformColors(style)
    
    return style