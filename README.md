# TextFic Wizard
The TextFic Wizard is an application for producing prettily-formatted texting 
fics to be published on AO3.  

It is designed to be easy-to-use, requiring only very basic changes to the 
source text to indicate where text message blocks appear.

It turns this:  

    ||| Besties
    Alice: Hi Frank!
    Frank: Hi, Alice!
    Frank: How are you?
    Alice: I'm good, thanks!
    /// Alice added Lily
    Lily: Hi guys!
    |||

Into this:  
![Example image](example.png)

##Using the tool
  
You can find the latest release of the tool 
[on GitHub here](https://github.com/settifora/textficwizard/releases).

The easiest way to run it is as follows:
1. Download the .exe file from the latest release (under "Assets")
2. Place it in an empty folder on your computer
3. Follow the instructions in the UserManual.pdf from the latest release  

Alternatively, you can download and run the Python source code. You will need to
install the module dependencies listed in requirements.txt (if you have pip, you
can do this with `pip install -r requirements.txt`).

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

## Acknowledgements
The formatting done by the wizard is based on the message formatting in 
[Did You Miss Me?](https://archiveofourown.org/works/36253849/chapters/90375916),
which is itself based on
[this tutorial](https://archiveofourown.org/works/6434845/chapters/14729722).

The wizard is built on the following libraries:
* [PyQt5](https://pypi.org/project/PyQt5/)
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
* [Mammoth](https://pypi.org/project/mammoth/)
* [PyQtWebEngine](https://pypi.org/project/PyQtWebEngine/)

Executable files for each release are produced using [PyInstaller](https://pypi.org/project/pyinstaller/).