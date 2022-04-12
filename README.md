# TextFic Wizard
The TextFic Wizard can be used to create prettily-formatted texting fics for the 
AO3 platform.  
  
The author writes the fic in simple English, with some very straightforward 
additions to mark the beginning and end of text message blocks. The wizard will
then convert the fic to HTML.  

The wizard also allows the author to easily configure text bubble colors for the 
characters within their fic.

### Limitations
The following limitations currently apply, **but are being actively worked on**:
* Character names in messages must be a single word containing only letters and 
numbers (no spaces or special characters).
* Each character can have only one name. If you want the same character to use 
different names in different chats, you will need to configure multiple 
"Characters" all using the same color.

Please also note the following:
* The current (beta) format required for input files is subject to change in 
future releases, and those changes may not be backwards compatible, meaning you 
may need to modify your input files for use with future versions of the wizard.

## Example usage
    ||| Example text block
    Alice: I am sending a message
    Bob: I am replying!
    Bob: How are you, Alice?
    /// Charlie has joined
    Charlie: I am here too!
    |||
  

The above document will produce output which looks something like this:
![Example image](example.png)
