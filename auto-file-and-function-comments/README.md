# Auto File and Function Comments README

This extension will allow you to add comments to your Python, Java, C/C++ (and header) files. All you have to do is have the file you want commented open, then press `Alt+W`. Please note that this extension assumes that your code has no syntax errors.

## Features

Adds file comments at the start for .py, .java, .c, .cpp, .h, and .hpp files.  Adds function comments in .py, .java, .h, and .hpp files.

# Languages Currently Supported (and Will be Supported in The Future)
&#x2611; C

&#x2611; C++

&#x2611; Java

&#x2611; Python

&#x2610; JavaScript

&#x2610; Other

## Extension Settings

This extension contributes the following settings:

* `auto-file-and-function-comments.author`: The author's name for the file(s) and function(s).

## Known Issues
- ~~Can not change author name in extension settings as intended~~
- Does not properly comment classes (with inheritance) in C++
- Does not properly comment classes (and class methods) in Python
- Currently overwrites previously generated comments if run more than once in the file

## Future Features

- Add comments for other programming languages
- Allow for comment rewrite or keep current comments for files/functions (determined by a user setting)
- Allow user to add more/customize default comment lines

## Release Notes

### 1.0.0

Initial release of auto-file-and-function-comments.

### 1.0.1

Added functionality for python files.

### 1.0.2
Fixed ability to change author name.

---

**Enjoy!**
