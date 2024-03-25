# Auto File and Function Comments README

This extension will allow you to add comments to your Python, Java, C/C++ (and header) files. All you have to do is have the file you want commented open, then press `Alt+W`. Please note that this extension assumes that your code has no syntax errors.

## Features

Adds file comments at the start for .py, .java, .c, .cpp, .h, and .hpp files.  Adds function comments in .py, .java, .h, and .hpp files. Allows user to add more/customize default comment lines.

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
* `auto-file-and-function-comments.comment-writer.date`: Include current date in file comments.
* `auto-file-and-function-comments.comment-writer.additional-file-comments`: 
Any additional file comments that you want to add right above the description. (each item will be on a seperate line).
* `auto-file-and-function-comments.comment-writer.additional-method-comments`: 
Any additional method comments that you want to add right below the description. (each item will be on a seperate line).
* `auto-file-and-function-comments.comment-writer.additional-adt-comments`: 
Any additional adt (like classes, structures, unions, enumerations, etc.) comments that you want to add right below the description. (each item will be on a seperate line).


## Known Issues
- Does not properly comment classes (with inheritance) in C++
- Does not properly comment classes (and class methods) in Python
- Currently overwrites previously generated comments if run more than once in the file


## Future Features
- Add comments for other programming languages.
- Allow for comment rewrite or keep current comments for files/functions (determined by a user setting).

## Release Notes

### 1.0.0

Initial release of auto-file-and-function-comments.

### 1.0.1

Added functionality for python files.

### 1.0.2
Fixed ability to change author name.

### 1.0.3
Added basic ability to comment C++ classes (still does not support inherited C++ classes). Added ability to decide to include the date in the file comments and add additional comment lines for file, method, and adt comments.

### 1.0.4
Fixed some formating errors from previous version.

### 1.0.5
Updated ReadMe and ChangeLog.

### 1.0.6
Python classes (both inherited and not) can be commented. Added logo for extension.

---

**Enjoy!**
