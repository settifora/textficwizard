import re

from common.definitions import getContrastColor, HEX_COLOR_REGEX

# Config validation regexes
CHARACTER_NAME_REGEX = re.compile('^[a-z0-9]+$')
CHARACTER_PRETTY_NAME_REGEX = re.compile('^[a-z0-9]+$')

# Class representing a character's config
class Character():
    # Constructor
    # Parameters: 
    #     name:       The name of the character
    #     color:      The character's text bubble background color
    #     fontColor:  The character's text bubble font color (optional)
    def __init__(self, name, color, fontColor=None):
        # Primary names are lowercase
        name = name.lower()
        
        # If the font color wasn't specified, figure out the best one to use
        # for contrast (black or white)
        if not fontColor:
            fontColor = getContrastColor(color)
            
        # Save the variables
        self.name = name
        self.color = color
        self.fontColor = fontColor
    
    # Method to get a dictionary containing the character config
    # Returns: dict
    def toDict(self):
        return self.__dict__
        
    # Method to get the pretty display name of the character
    # Returns: str
    def getDisplayName(self):
        return self.name.capitalize()
    
    # Method to check whether this object contains valid config values
    # Returns: boolean
    def isValid(self):
        valid = True

        if not CHARACTER_NAME_REGEX.fullmatch(self.name):
            valid = False        
        elif not HEX_COLOR_REGEX.fullmatch(self.color):
            valid = False
        
        return valid
        
    # Static method to get a Character object from the values in the given dict
    # Returns: Character
    def fromDict(dict):
        return Character(dict['name'], dict['color'], dict['fontColor'])