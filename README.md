# Auto File and Function Comments README

This extension will allow you to add comments to your Python, Java, C/C++ (and header) files. All you have to do is have the file you want commented open, then press `Alt+W`. Please note that this extension assumes that your code has no syntax errors.

## Features

Adds file comments at the start for .py, .java, .c, .cpp, .h, and .hpp files.  Adds function comments in .py, .java, .h, and .hpp files. Allows user to add more/customize default comment lines.

# Languages Currently Supported (and will be supported in the future)
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

### Custom Variables for Settings
- `%file_name%`: The file name, excludes the file extension.
- `%file_extension%`: The file extension.
- `%author%`: The author of the code block.
- `%date%`: The current date when the comments are generated.
- `%class_name%`: The name of the class. Defaults to "Not Found" if the class name doesn't exist or couldn't be found.
- `%return_type%`: The return type of the method. Defaults to "Not Found" if the return type doesn't exist or couldn't be found.
- `%[]...%`: If any variable values inside of the [] are lists, the data inside of the [] will be repeated for the whole list. If a variable isn't a list, it will just be repeated for each [] instance. If there 2 or more lists present in the [] and 1 of the lists is longer than the others, for the shorter lists, "Not Found" will be printed after all items in that list has been printed. If any list has 0 items in it, "N/A" will be printed. Below are some specific variables/commands that can be used inside of []:
    - `%s=%`: specifies the seperator for the list, e.g. %s=\\n% means everything in the [] is seperated by a new line.
    - `%access_specifier%`: The access specifier of the current class. Defaults to "Not Found" if an access specifier doesn't exist or couldn't be found.
    - `%parent_class_name%`: The name of the parent/base class. Defaults to "Not Found" if a parent/base class doesn't exist or couldn't be found.
    - `%parent_access_specifier%`: The access specifier of the parent/base class. Defaults to "Not Found" if an access specifier doesn't exist or couldn't be found.
    - `%parameter_name%`: The name of the parameter. Defaults to "Not Found" if a parameter name doesn't exist or couldn't be found.
    - `%parameter_type%`: The type of the parameter. Defaults to "Not Found" if a parameter type doesn't exist or couldn't be found.

#### Example 1 ***Notes: file name with extension is TestFile.cpp or TestFile.java or test_file.py and author is Brooke Cronin***
<details>
<summary>C/C++</summary>

User Defined Format for File Comments:
```
@file %file_name%
@author %author%
@brief
```

Comments Generated:
```
/// @file TestFile
/// @author Brooke Cronin
/// @brief
```
</details>

<details>
<summary>Java</summary>

User Defined Format for File Comments:
```
File Name: %file_name%
File Author: %author%
Description: 
```

Comments Generated:
```
/*
 * File Name: TestFile
 * File Author: Brooke Cronin
 * Description: 
*/
```
</details>

<details>
<summary>Python</summary>

User Defined Format for File Comments:
```
File Name: %file_name%
File Author: %author%
Description: 
```

Comments Generated:
```
"""
File Name: test_file
File Author: Brooke Cronin
Description: 
"""
```
</details>

#### Example 2a ***Notes: author is Brooke Cronin, method name is sum, method has three parameters (int a, int b, double c), and returns double value***
<details>
<summary>C/C++</summary>

User Defined Format for Method Comments:
```
@brief 
@author %author%
%[@param %parameter_name% (%parameter_type%)%s=\\n%]...%
@return %return_type%
```

Comments Generated:
```
/// @brief 
/// @author Brooke Cronin
/// @param a (int)
/// @param b (int)
/// @param c (double)
/// @return double
```
</details>

<details>
<summary>Java</summary>

User Defined Format for Method Comments:
```
Method Name: %method_name%
Description: Written by: %author%
Parameters: %[(%parameter_type%) %parameter_name%%s=, %]...%
Returns: %return_type%
```

Comments Generated:
```
/*
 * Method Name: sum
 * Description: Written by: Brooke Cronin
 * Parameters: a(int), b(int), c(double)
 * Returns: double
*/
```
</details>

<details>
<summary>Python</summary>

User Defined Format for Method Comments:
```
Method Name: %method_name%
Description: Written by: %author%
### Parameters
%[- %parameter_name%: %parameter_type%%s=\\n%]...%
### Returns
- %return_type%
```

Comments Generated:
```
"""
Method Name: sum
Description: Written by: Brooke Cronin
### Parameters
- a: int
- b: int
- c: double
### Returns
- double
"""
```
</details>

#### Example 2b ***Notes: author is Brooke Cronin, method name is hello_world, method has no parameters, and returns nothing***
<details>
<summary>C/C++</summary>

User Defined Format for Method Comments:
```
@brief 
@author %author%
%[@param %parameter_name% (%parameter_type%)%s=/n%]...%
@return %return_type%
```

Comments Generated:
```
/// @brief 
/// @author Brooke Cronin
/// @param N/A (N/A)
/// @return Not Found
```
</details>

<details>
<summary>Java</summary>

User Defined Format for Method Comments:
```
Method Name: %method_name%
Description: Written by: %author%
Parameters: %[(%parameter_type%) %parameter_name%%s=, %]...%
Returns: %return_type%
```

Comments Generated:
```
/*
 * Method Name: hello_world
 * Description: Written by: Brooke Cronin
 * Parameters: (N/A) N/A
 * Returns: Not Found
*/
```
</details>

<details>
<summary>Python</summary>

User Defined Format for Method Comments:
```
Method Name: %method_name%
Description: Written by: %author%
### Parameters
%[- %parameter_name%: %parameter_type%%s=\\n%]...%
### Returns
- %return_type%
```

Comments Generated:
```
"""
Method Name: hello_world
Description: Written by: Brooke Cronin
### Parameters
- N/A: N/A
### Returns
- Not Found
"""
```
</details>

#### Example 2c ***Notes: author is Brooke Cronin, method name is __init__ or Person, method belongs to the Person class, method has 4 parameters (Person self, str first_name, str last_name, and int age), and returns None or void***
<details>
<summary>C/C++</summary>

User Defined Format for Method Comments:
```
@brief 
@author %author%
%[@param %parameter_name% (%parameter_type%)%s=/n%]...%
@return %return_type%
```

Comments Generated:
```
/// @brief 
/// @author Brooke Cronin
/// @param self (Person)
/// @param first_name (str)
/// @param last_name (str)
/// @param age (int)
/// @return void
```
</details>

<details>
<summary>Java</summary>

User Defined Format for Method Comments:
```
Method Name: %method_name%
Description: Written by: %author%
Parameters: %[(%parameter_type%) %parameter_name%%s=, %]...%
Returns: %return_type%
```

Comments Generated:
```
/*
 * Method Name: Person
 * Description: Written by: Brooke Cronin
 * Parameters: (String) firstName, (String) lastName, (int) age
 * Returns: void
*/
```
</details>

<details>
<summary>Python</summary>

User Defined Format for Method Comments:
```
Method Name: %method_name%
Description: Written by: %author%
### Parameters
%[- %parameter_name%: %parameter_type%%s=\\n%]...%
### Returns
- %return_type%
```

Comments Generated:
```
"""
Method Name: __init__
Description: Written by: Brooke Cronin
### Parameters
- self: Person
- first_name: str
- last_name: str
- age: int
### Returns
- None
"""
```
</details>

#### Example 3a ***Notes: author is Brooke Cronin and class name is Person***
<details>
<summary>C++</summary>

User Defined Format for ADT Comments:
```
@brief 
@author %author%
```

Comments Generated:
```
/// @brief 
/// @author Brooke Cronin
```
</details>

<details>
<summary>Java</summary>

User Defined Format for ADT Comments:
```
Class Name: %class_name%
Description: Written by: %author%
```

Comments Generated:
```
/*
 * Class Name: Person
 * Description: Written by: Brooke Cronin
*/
```
</details>

<details>
<summary>Python</summary>

User Defined Format for ADT Comments:
```
Class Name: %class_name%
Description: Written by: %author%
```

Comments Generated:
```
"""
Class Name: Person
Description: Written by: Brooke Cronin
"""
```
</details>

#### Example 3b ***author is Brooke Cronin, class name is Teacher, and this class is a child class to the Person class***

<details>
<summary>C++</summary>

User Defined Format for ADT Comments:
```
@class: %class_name%
@brief: Written by: %author%
Inherits from:
%[- %parent_class%: %parent_access_specifier%%s=\\n%]...%
```

Comments Generated:
```
/// @class: Teacher
/// @brief: Written by: Brooke Cronin
/// Inherits from:
/// - Person: public
```
</details>

<details>
<summary>Java</summary>

User Defined Format for ADT Comments:
```
Class Name: %class_name%
Description: Written by: %author%
Inherits from:
%[- %parent_class%: %parent_access_specifier%%s=\\n%]...%
```

Comments Generated:
```
/*
 * Class Name: Person
 * Description: Written by: Brooke Cronin
 * Inherits from:
 * - Person: public
*/
```
</details>

<details>
<summary>Python</summary>

User Defined Format for ADT Comments:
```
Class Name: %class_name%
Description: Written by: %author%
Inherits from:
%[- %parent_class%: %parent_access_specifier%%s=\\n%]...%
```

Comments Generated:
```
"""
Class Name: Person
Description: Written by: Brooke Cronin
Inherits from:
- Person: public
"""
```
</details>

## Known Issues
- Currently overwrites previously generated comments if run more than once in the file


## Future Features
- Add comments for other programming languages.
- Allow for comment rewrite or keep current comments for files/functions (determined by a user setting).
- Allow user to have different preferences/user settings for each language.

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
Python classes (both inherited and not) can be commented. C++ classes (both inherited and not) can be commented. Added logo for extension.

### 1.0.7
Updated ReadMe and ChangeLog.

### 2.0.0
Can now have specific comment formats for each language, and a default.

---

**Enjoy!**
