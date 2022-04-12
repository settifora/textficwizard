from bs4 import BeautifulSoup
import re
import os
from config.manager import getConfigManager, OUTPUT_DIR
import mammoth
from common.definitions import *

# Method to wrap the given element in a <span> with the specified class
# Parameters:
#     element:      The element to wrap
#     classString:  The class to use for the parent <span>
# Returns: bs4.element.Tag  The parent <span> wrapping the element
def wrapWithClass(soup, element, classString):
    element.wrap(soup.new_tag('span'))
    parentSpan = element.parent
    addClass(soup, parentSpan, classString)

    return parentSpan

# Method to insert a line break (<br> tag) into the given element at a specified
# position. If the position is -1, add it to the end.
# Parameters:
#     parent:    The parent into which to insert the break
#     hidden:    Whether the break should have the 'hide' class set
#     position:  The position at which to insert the break
def insertBreak(soup, parent, hidden, position):
    breakTag = soup.new_tag('br')

    if position == -1:
        parent.append(breakTag)
    else:
        parent.insert(position, breakTag)

    if hidden:
        wrapWithClass(soup, breakTag, 'hide')

# Method to add a class to a tag, preserving any classes which already exist
# Parameters:
#     element:      The tag
#     classString:  The class to add
def addClass(soup, element, classString):
    element['class'] = ' '.join([element.get('class', ''), classString])

# Method to end the given speaker block, adding it to the message block. Sets
# "bottom-text" class on the last message in the block, which allows the "tail"
# to be displayed on the last message from a given sender.
# Parameters:
#     speakerBlock:  The speaker block to end
#     messageBlock:  The parent message block
def endSpeakerBlock(soup, speakerBlock, messageBlock):
    if speakerBlock:
        addClass(soup, speakerBlock.find_all('span')[-1], 'bottom-text')
        insertBreak(soup, speakerBlock, True, -1)
        messageBlock.append(speakerBlock)

# Method to start a new speaker block, which is a <span> tag containing a series
# of messages from a single  sender. Initiates the tag, styles it appropriately
# (taking into account whether the sender is the 'group leader', whose messages
# appear on the right). Also adds a name-tag containing the sender's name,
# and then first message.
# Parameters:
#     message:      The first message to be added to the block
#     sender:       The name of the sender
#     groupLeader:  The 'group leader' for the message block
# Returns: bs4.element.Tag  The speaker block
def startSpeakerBlock(soup, message, sender, groupLeader):
    speakerBlock = soup.new_tag('span')
    speakerBlock['class'] = 'sender-block ' + sender.lower()
    if (sender == groupLeader):
        speakerBlock['class'] = speakerBlock['class'] + ' group-leader'
    addClass(soup, message, 'top-text')
    nameTag = soup.new_tag('span')
    nameTag['class'] = 'name-tag'
    nameTag.string = sender
    speakerBlock.append(nameTag)
    nameTag.wrap(soup.new_tag('strong'))
    insertBreak(soup, speakerBlock, False, -1)
    speakerBlock.append(message)
    insertBreak(soup, speakerBlock, False, -1)

    return speakerBlock

# Method to process a given .docx file
# Parameters:
#     filename:  The path of the file to process
# Returns: [str, set(str)]  The output file path (str), and a set of names of
#     senders of messages identified in this file
def processFile(filename):
    # Get the file contents and convert to HTML (using mammoth library)
    with open(filename, 'rb') as docxFile:
        result = mammoth.convert_to_html(docxFile)
        htmlDoc = result.value

    # Parse the HTML to BeautifulSoup
    soup = BeautifulSoup(htmlDoc, 'html.parser', multi_valued_attributes=None)

    # Keep track of any characters we find sending messages
    characters = set()

    # Find all instances of the "|||" delimiter string used to denote the start
    # and end of text blocks
    textDelimiters = soup.find_all(string=re.compile('\|\|\|'))

    # If delimiters still exist, we still have text blocks to process - do that
    while textDelimiters:
        # Get the message block header paragraph (starts with "|||")
        blockStart = textDelimiters[0]
        parentPara = blockStart.find_parent('p')

        # Replace the paragraph with a styled span
        messagesHeader = wrapWithClass(soup, parentPara, 'messages-header')

        # Add a 'chat name' prefix to the message header
        chatNameSpan = soup.new_tag('span')
        chatNameSpan.string = 'Chat name: '
        addClass(soup, chatNameSpan, 'hide')
        parentPara.insert(0, chatNameSpan)

        # Get rid of the parent paragraph
        parentPara.wrap(soup.new_tag('strong'))
        parentPara.unwrap()

        # Strip out the "|||" delimiter from the header
        blockStart.replace_with(blockStart.strip('| '))

        # Build a list of messages we need to process - i.e. everything until
        # the next "|||" line
        messagesInBlock = []
        for sibling in messagesHeader.find_next_siblings('p'):
            if sibling.get_text().startswith('|||'):
                sibling.decompose()
                break
            else:
                messagesInBlock.append(sibling)

        # The person who sends the first message is assigned as the "group
        # leader" - their texts appear on the right
        groupLeader = None

        # Set up a container for all the messages in this block
        messageContainer = soup.new_tag('span')
        messageContainer['class'] = 'message-block'

        # Keep track of the currently active speaker and their message block
        speakerBlock = None
        lastSender = None

        # Loop through and process the messages
        for message in messagesInBlock:
            # For our purposes, the interesting 'content' is the first bit of
            # text within the tag
            content = next(message.strings)

            # See if we've got a comment
            if (content).startswith('///'):
                # Whoever was speaking has been interrupted
                if speakerBlock:
                    endSpeakerBlock(soup, speakerBlock, messageContainer)
                    speakerBlock = None

                # Handle the comment - wrap it in a styled <span> and ditch the
                # <p> and "///"
                wrappedMessage = wrapWithClass(soup, message, 'message-action')
                message.wrap(soup.new_tag('i'))
                message.unwrap()
                content.replace_with(content.strip('/ '))
                messageContainer.append(wrappedMessage)
                insertBreak(soup, messageContainer, True, -1)
                insertBreak(soup, messageContainer, True, -1)

                # This was a comment so we're done processing it
                continue

            # If we've got here, we've got a message (not a comment) - style it
            # as such
            wrappedMessage = wrapWithClass(soup, message, 'message')
            message.unwrap()

            # Find out who sent the message (it should start with their name,
            # followed by ": ")
            result = re.match(r'([A-Za-z0-9]+?): .+', content)

            # If this doesn't seem to be a message, the safest thing to do is to
            # skip it
            if not result:
                continue

            # Get the sender (we've already captured it, just assign it a nice
            # name)
            sender = result.group(1)

            # Add the speaker to our running list
            characters.add(sender)

            # Strip the sender name from the message (this is crude but
            # effective)
            content.replace_with(content[len(sender) + 2:])

            # If we don't have a main author yet, this sender can have the role
            if not groupLeader:
                groupLeader = sender

            # If this is a new sender, close out the speaker block and start a
            # new one
            if (not sender == lastSender):
                endSpeakerBlock(soup, speakerBlock, messageContainer)
                speakerBlock = startSpeakerBlock(soup,
                                                 wrappedMessage,
                                                 sender,
                                                 groupLeader)
                lastSender = sender
            else:
                # Otherwise, add the message to the current speaker block
                speakerBlock.append(wrappedMessage)
                insertBreak(soup, speakerBlock, False, -1)

        # We're done processing messages - close out the last speaker block
        endSpeakerBlock(soup, speakerBlock, messageContainer)

        # Add the message container to the HTML and move the header inside it
        messagesHeader.insert_after(messageContainer)
        insertBreak(soup, messageContainer, True, 0)
        messageContainer.insert(1, messagesHeader)
        insertBreak(soup, messageContainer, True, 2)
        insertBreak(soup, messageContainer, True, 3)

        # Add a "delimiter bar" (which we'll style to act as a spacer) after the
        # message block
        delimiterBox = soup.new_tag('span')
        delimiterBox['class'] = 'delimiter-bar'
        messageContainer.append(delimiterBox)

        # Pop the whole message block in a paragraph tag, else AO3 gets upset
        messageContainer.wrap(soup.new_tag('p'))

        # Re-scan for "|||" delimiters
        textDelimiters = soup.find_all(string=re.compile('\|\|\|'))

    # We're done! Output the result to a file.
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    outfilePath = os.path.join(OUTPUT_DIR,
                               os.path.basename(filename)[:-5] + '.txt')

    with open(outfilePath, 'w') as outfile:
        outfile.write(soup.prettify())
        outfile.close()

    # Return a list of character names from this document
    return [outfilePath, characters]
