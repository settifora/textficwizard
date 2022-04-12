import json
import os
from config.classes import *
from common.definitions import *

# Project config - singleton instance
configManager = None

# File path to persistent project config
JSON_FILE_PATH = 'config.json'

# Singleton class - config manager
class ConfigManager():
    # Constructor
    def __init__(self):
        self.characterConfig = {}
        self.loadConfig()
        
    # Method to load config from JSON persistent storage
    def loadConfig(self):
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r') as charfile:
                self.characterConfig = json.load(charfile)
                charfile.close()

    # Method to save config to JSON persistent storage
    def saveConfig(self):
        with open(JSON_FILE_PATH, 'w') as charfile:
            json.dump(self.characterConfig, charfile)
            charfile.close()
            generateCss()
    
    # Method to list all characters in the current config
    # Returns: [] of Characters
    def listCharacters(self):
        characters = []
        for name in self.characterConfig:
            character = Character.fromDict(self.characterConfig[name])
            characters.append(character)
            
        return characters
    
    # Method to get a particular character's config by name
    # Parameters:
    #     name:  The character's name
    # Returns: Character
    def getCharacter(self, name):
        character = None
        if (name.lower() in self.characterConfig):
            character = Character.fromDict(self.characterConfig[name.lower()])
        return character
    
    # Method to add a character
    # Parameters:
    #     name:   The name of the character
    #     color:  The text bubble color for the character
    # Returns: boolean (whether the provided config was valid)
    def addCharacter(self, name, color):
        character = Character(name, color)
    
        valid = character.isValid()
        
        if valid:
            self.characterConfig[character.name] = character.toDict()
            self.saveConfig()
            
        return valid
    
    # Method to delete a character
    # Parameters:
    #     name:   The name of the character
    # Returns: boolean (whether the character existed and was deleted)
    def deleteCharacter(self, name):
        removed = self.characterConfig.pop(name.lower(), None)
        self.saveConfig()
        return removed
 

# Function to get singleton ConfigManager instance, creating it if necessary
# Returns: ConfigManager
def getConfigManager():
    global configManager
    if configManager is None:
        configManager = ConfigManager()
    return configManager
    
# Function to generate character-specific CSS for the given character
# Returns: str  The generated CSS
def getCharacterCss(name, color, fontColor):
    cssClasses = CSS_CHARACTER_CLASSES
    cssClasses = cssClasses.replace('CHARACTER_NAME', name)
    cssClasses = cssClasses.replace('CHARACTER_COLOR', color)
    cssClasses = cssClasses.replace('CHARACTER_FONT', fontColor)
    return cssClasses
 
# Function to combine character-specific and base CSS, and output it to file
def generateCss():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(os.path.join(OUTPUT_DIR,CSS_FILE_NAME), 'w') as outfile:
        outfile.write(BASE_CSS_CLASSES)

        for character in getConfigManager().listCharacters():
            outfile.write(getCharacterCss(character.name,
                                          character.color,
                                          character.fontColor))

        outfile.close()