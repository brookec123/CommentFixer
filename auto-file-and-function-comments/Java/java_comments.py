import argparse
import os
import regex as re
from typing import List
from datetime import datetime

def generate_method_comments(method_name: str, method_author: str, return_type: str, parameters: List[str], additional_method_comments: List[str]) -> str:
    method_comments = ""
    method_comments += ("/*"+"\n")
    method_comments += (" * Method Name: "+method_name+"\n")
    method_comments += (" * Method Author: "+method_author+"\n")
    for comment in additional_method_comments:
        method_comments += (" * " + comment + "\n")
    method_comments += (" * Description: "+"\n")
    method_comments += (" * Method Parameters: ")
    param = list(parameters[1])
    method_comments += ("("+param[0]+")"+" "+param[1])
    for index in range(2, len(parameters)):
        param = list(parameters[index])
        method_comments += (", ("+param[0]+")"+" "+param[1])
    method_comments += ("\n")
    method_comments += (" * Method Return Type: "+return_type+"\n")
    method_comments += (" */"+"\n")
    return method_comments

def generate_file_comments(file_name: str, file_author: str, include_date: bool, additional_file_comments: List[str], additional_adt_comments: List[str]) -> str:
    file_comments = ""
    file_comments += ("/*"+"\n")
    file_comments += (" * File Name: "+file_name+"\n")
    file_comments += (" * File Author: "+file_author+"\n")
    if include_date:
        file_comments += (" * Date: "+datetime.today().strftime('%Y-%m-%d')+"\n")
    for comment in additional_file_comments:
        file_comments += (" * " + comment + "\n")
    for comment in additional_adt_comments:
        file_comments += (" * " + comment + "\n")
    file_comments += (" * Description: "+"\n")
    file_comments += (" */"+"\n\n")
    
    return file_comments

def create_additional_comment_list(comments: str) -> List[str]:
    return comments.split("\\~\\`/~/")

def handle_arguments():
    parser = argparse.ArgumentParser(description="", usage="python java_comments.py (--file <file_location> | --folder <folder_location>) --author <author>")
    file_folder_group = parser.add_mutually_exclusive_group(required=True)
    file_folder_group.add_argument("--file", dest="file_location", type=str, help="full .java file location that needs to be commented")
    file_folder_group.add_argument("--folder", dest="folder_location", type=str, help="folder containing all .java files that need to be commented")
    parser.add_argument("--author", dest="author", type=str, required=True, help="author of the .h file")
    parser.add_argument("--date", dest="date", type=str, required=True, help="whether the date that the file comments was created on should be added")
    parser.add_argument("--additional-file-comments", dest="additional_file_comments", type=str, required=True, help="all additional comments the user wants to add to the file comments")
    parser.add_argument("--additional-method-comments", dest="additional_method_comments", type=str, required=True, help="all additional comments the user wants to add to the method comments")
    parser.add_argument("--additional-adt-comments", dest="additional_adt_comments", type=str, required=True, help="all additional comments the user wants to add to the adt comments")
    
    args = parser.parse_args()
    if args.file_location:
        main(args.file_location, args.author, args.date, create_additional_comment_list(args.additional_file_comments), create_additional_comment_list(args.additional_method_comments), create_additional_comment_list(args.additional_adt_comments))
    elif args.folder_location:
        if not os.path.isdir(args.folder_location):
            print(f"The specified path '{args.folder_location}' is not a valid directory.")
            return
        for filename in os.listdir(args.folder_location):
            if filename.endswith(".h") or filename.endswith(".c") or filename.endswith(".cpp"):
                file_path = os.path.join(args.folder_location, filename)
                main(file_path, args.author, args.date, create_additional_comment_list(args.additional_file_comments), create_additional_comment_list(args.additional_method_comments), create_additional_comment_list(args.additional_adt_comments))

def main(file_location: str, author: str, include_date: str, additional_file_comments: List[str], additional_method_comments: List[str], additional_adt_comments: List[str]) -> None:
    if include_date == "true":
        include_date = True
    else:
        include_date = False
    file_name, _ = os.path.splitext(os.path.basename(file_location))
    lines = []
    file_comments_generated = False
    method_comments_generated = False
    inside_of_class = False
    main_method_start = "publicstaticvoidmain(String[]args)"
    method_start_pattern = r"^\s+(\w+)\s+(\w+)\("
    method_param_pattern = r"(\w+)\s+(\w+)"
    with open(file_location, "r") as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            if len(lines[i].strip()) != 0 and not file_comments_generated:
                if lines[i].startswith("/*"):
                    file_comments_generated = True
                    pass
                else:
                    file_comments = generate_file_comments(file_name, author, include_date, additional_file_comments, additional_adt_comments)
                    lines.insert(i, file_comments)
                    file_comments_generated = True
            if file_comments_generated and not inside_of_class:
                if " class " in lines[i]:
                    inside_of_class = True
            if inside_of_class:
                if "}" in lines[i] and method_comments_generated:
                    method_comments_generated = False
                if not main_method_start in lines[i].strip() and not method_comments_generated:
                    method_line = lines[i]
                    method_line = method_line.replace("public ", "")
                    method_line = method_line.replace("private ", "")
                    method_line = method_line.replace("static ", "")
                    match = re.match(method_start_pattern, method_line)
                    if match:
                        method_comments = generate_method_comments(match.group(2), author, match.group(1), re.findall(method_param_pattern, lines[i]), additional_method_comments)
                        method_comments_generated = True
                        lines.insert(i, method_comments)
            i += 1
                           
    with open(file_location, "w") as f:              
        for i in lines:
            f.write(str(i))

if __name__ == "__main__":
    handle_arguments()
    
    
    
    
# import argparse
# import os
# import re
# from typing import List
# from datetime import datetime

# ACCESS_SPECIFIERS = ["", "public", "private", "protected", "final"]

# def generate_class_comments(class_author: str, base_class_name: List[str], class_name: str, additional_adt_comments: List[str]) -> str:
#     class_comments = ""
#     if base_class_name != []:
#         for base in base_class_name:
#             class_comments += ("/// Base Class Name: "+base[1]+" ("+base[0]+")\n")
#     class_comments += ("/// Class Name: "+class_name+"\n")
#     class_comments += ("/// Class Author: "+class_author+"\n")
#     if additional_adt_comments[0] != "":
#         for comment in additional_adt_comments:
#             class_comments += ("/// " + comment + "\n")
#     class_comments += ("/// Description: ")
#     return class_comments

# def add_class_comments(lines: List[str], author: str, additional_adt_comments: List[str], additional_method_comments: List[str]) -> List[str]:
#     constructor_comments_generated = set()
#     destructor_comments_generated = set()
#     inside_class = False
#     class_name = ""
#     class_no_inheritance_start_pattern = r"^" + "|".join(map(re.escape, ACCESS_SPECIFIERS)) + r" class ([a-zA-Z0-9\*]+)\s*(\{|$)"
#     class_with_inheritance_start_pattern = r"^" + "|".join(map(re.escape, ACCESS_SPECIFIERS)) + r"class ([a-zA-Z0-9\*]+)\s*extends "
#     base_class_pattern = r"" + "|".join(map(re.escape, ACCESS_SPECIFIERS)) + r"\s+([a-zA-Z0-9\*]+)"
#     class_end_pattern = r"\}\s*$"
#     constructor_start_pattern = rf"^\s*{class_name}\("
#     destructor_start_pattern = rf"^\s*~{class_name}\("
#     method_param_pattern = r"([a-zA-Z0-9\*]+)\s+([a-zA-Z0-9\*]+)"
#     i = 0
#     while i < len(lines):
#         match_class_no_inheritance_start = re.match(class_no_inheritance_start_pattern, lines[i])
#         match_class_end = re.match(class_end_pattern, lines[i])
#         match_class_with_inheritance_start = re.match(class_with_inheritance_start_pattern, lines[i])
        
#         if match_class_no_inheritance_start and not inside_class:
#             class_name = lines[i].replace("class", "")
#             class_name = class_name.replace("{", "")
#             class_name = class_name.strip()
#             lines.insert(i, generate_class_comments(author, [], class_name, additional_adt_comments))
#             inside_class = True
#             constructor_start_pattern = rf"^\s*{class_name}\("
#             destructor_start_pattern = rf"^\s*~{class_name}\("
#         elif match_class_with_inheritance_start and not inside_class:
#             line = lines[i]
#             line = lines[i].replace("class", "")
#             line = line.replace("{", "")
#             line = line.strip()
#             class_name = line[0:line.index(":")]
#             base_class_string = line[line.index(":")+1:]
#             lines.insert(i, generate_class_comments(author, re.findall(base_class_pattern, base_class_string), class_name, additional_adt_comments))
#             inside_class = True
#             constructor_start_pattern = rf"^\s*{class_name}\("
#             destructor_start_pattern = rf"^\s*~{class_name}\("
#         elif inside_class:
#             match_constructor_start = re.match(constructor_start_pattern, lines[i])
#             match_destructor_start = re.match(destructor_start_pattern, lines[i])
#             if match_class_end:
#                 class_name = ""
#                 inside_class = False
#             elif match_constructor_start and lines[i] not in constructor_comments_generated:
#                 constructor_comments_generated.add(lines[i])
#                 lines.insert(i, generate_method_comments(author, "", re.findall(method_param_pattern, lines[i]), additional_method_comments))
#             elif match_destructor_start and lines[i] not in destructor_comments_generated:
#                 destructor_comments_generated.add(lines[i])
#                 lines.insert(i, generate_method_comments(author, "", re.findall(method_param_pattern, lines[i]), additional_method_comments))
#         i += 1
#     return lines

# def generate_method_comments(method_author: str, return_type: str, parameters: List[str], additional_method_comments: List[str]) -> str:
#     method_comments = ""
#     method_comments += ("\n/// @brief ")
#     method_comments += ("\n/// @author "+method_author)
#     if additional_method_comments[0] != "":
#         for comment in additional_method_comments:
#             method_comments += ("\n/// " + comment)
#     if return_type != "":
#         parameters.pop(0)
#     for param in parameters:
#         print("0", param[0])
#         method_comments += ("\n/// @param "+param[1]+" ("+param[0]+")")
#     if return_type != "":
#         method_comments += ("\n/// @return (" + return_type + ")")
#     return method_comments

# def add_method_comments(lines: List[str], author: str, additional_method_comments: List[str]) -> List[str]:
#     method_comments_generated = set()
#     prev_method = ""
#     method_start_pattern = r"^\s*(\S+)\s+(\S+)\("
#     method_param_pattern = r"([a-zA-Z0-9\*]+)\s+([a-zA-Z0-9\*]+)"
#     for i in reversed(range(len(lines))):
#         match = re.match(method_start_pattern, lines[i])
#         if match and lines[i] != prev_method and match.group(2) not in method_comments_generated:
#             prev_method = lines[i]
#             parameters = re.findall(method_param_pattern, lines[i])
#             return_type = (parameters[0])[0]
#             print(parameters)
#             method_comments = generate_method_comments(author, return_type, parameters, additional_method_comments)
#             lines.insert(i, method_comments)

#     return lines

# def generate_file_comments(file_name: str, file_author: str, include_date: bool, additional_file_comments: List[str]) -> str:
#     file_comments = ""
#     file_comments += ("/// File Name: "+file_name+"\n")
#     file_comments += ("/// File Author: "+file_author+"\n")
#     if include_date:
#         file_comments += ("/// Date: "+datetime.today().strftime("%Y-%m-%d")+"\n")
#     if additional_file_comments[0] != "":
#         for comment in additional_file_comments:
#             file_comments += ("/// " + comment + "\n")
#     file_comments += ("/// Description: ")
    
#     return file_comments

# def remove_previous_comments(lines: List[str]) -> List[str]:
#     new_lines = []
#     for line in lines:
#         if not line.lstrip().startswith("/*") and not line.lstrip().startswith("*") and not line.lstrip().startswith("*/") and not line.lstrip().startswith("///"):
#             new_lines.append(line)
#     return new_lines

# def create_additional_comment_list(comments: str) -> List[str]:
#     return comments.split("\\~\\`/~/")

# def handle_arguments() -> None:
#     parser = argparse.ArgumentParser(description="", usage="python c_comments.py (--file <file_location> | --folder <folder_location>) --author <author>")
#     file_folder_group = parser.add_mutually_exclusive_group(required=True)
#     file_folder_group.add_argument("--file", dest="file_location", type=str, help="full .h file location that needs to be commented")
#     file_folder_group.add_argument("--folder", dest="folder_location", type=str, help="folder containing all .c and .h files that need to be commented")
#     parser.add_argument("--author", dest="author", type=str, required=True, help="author of the .h file")
#     parser.add_argument("--date", dest="date", type=str, required=True, help="whether the date that the file comments was created on should be added")
#     parser.add_argument("--additional-file-comments", dest="additional_file_comments", type=str, required=True, help="all additional comments the user wants to add to the file comments")
#     parser.add_argument("--additional-method-comments", dest="additional_method_comments", type=str, required=True, help="all additional comments the user wants to add to the method comments")
#     parser.add_argument("--additional-adt-comments", dest="additional_adt_comments", type=str, required=True, help="all additional comments the user wants to add to the adt comments")

#     args = parser.parse_args()
#     if args.file_location:
#         main(args.file_location, args.author, args.date, create_additional_comment_list(args.additional_file_comments), create_additional_comment_list(args.additional_method_comments), create_additional_comment_list(args.additional_adt_comments))
#     elif args.folder_location:
#         if not os.path.isdir(args.folder_location):
#             print(f"The specified path '{args.folder_location}' is not a valid directory.")
#             return

#     for filename in os.listdir(args.folder_location):
#         if filename.endswith(".java"):
#             file_path = os.path.join(args.folder_location, filename)
#             main(file_path, args.author, args.date, create_additional_comment_list(args.additional_file_comments), create_additional_comment_list(args.additional_method_comments), create_additional_comment_list(args.additional_adt_comments))   

# def main(file_location: str, author: str, include_date: str, additional_file_comments: List[str], additional_method_comments: List[str], additional_adt_comments: List[str]) -> None:
#     if include_date == "true":
#         include_date = True
#     else:
#         include_date = False
#     file_name, file_extension = os.path.splitext(os.path.basename(file_location))
#     file_name += file_extension
#     with open(file_location, "r") as f:
#         lines = [line.rstrip("\n") for line in f]
#     lines = remove_previous_comments(lines)
#     file_comments = generate_file_comments(file_name, author, include_date, additional_file_comments)
#     lines.insert(0, file_comments)
    
#     lines = add_class_comments(lines, author, additional_adt_comments, additional_method_comments)
#     lines = add_method_comments(lines, author, additional_method_comments)

#     with open(file_location, "w") as f:
#         for line in lines:
#             f.write(line + "\n")

# if __name__ == "__main__":
#     handle_arguments()