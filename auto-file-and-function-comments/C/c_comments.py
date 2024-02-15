import argparse
import os
import re
from typing import List
from datetime import datetime

def generate_class_comments(class_author: str, class_name: str) -> str:
    class_comments = ""
    class_comments += ("/// Class Name: "+class_name+"\n")
    class_comments += ("/// Class Author: "+class_author+"\n")
    class_comments += ("/// Description: ")
    return class_comments

def add_class_comments(lines: List[str], author: str) -> List[str]:
    constructor_comments_generated = set()
    destructor_comments_generated = set()
    inside_class = False
    class_name = ""
    class_no_inheritance_start_pattern = r"^class ([^\(\)\s]+)\s*(\{|$)"
    class_end_pattern = r"\};\s*$"
    constructor_start_pattern = rf"^\s*{class_name}\("
    destructor_start_pattern = rf"^\s*~{class_name}\("
    method_param_pattern = r"([a-zA-Z0-9\*]+)\s+([a-zA-Z0-9\*]+)"
    i = 0
    while i < len(lines):
        match_class_no_inheritance_start = re.match(class_no_inheritance_start_pattern, lines[i])
        match_class_end = re.match(class_end_pattern, lines[i])
        if match_class_no_inheritance_start and not inside_class:
            class_name = lines[i].replace("class", "")
            class_name = class_name.replace("{", "")
            class_name = class_name.strip()
            lines.insert(i, generate_class_comments(author, class_name))
            inside_class = True
            constructor_start_pattern = rf"^\s*{class_name}\("
            destructor_start_pattern = rf"^\s*~{class_name}\("
        elif inside_class:
            match_constructor_start = re.match(constructor_start_pattern, lines[i])
            match_destructor_start = re.match(destructor_start_pattern, lines[i])
            if match_class_end:
                class_name = ""
                inside_class = False
            elif match_constructor_start and lines[i] not in constructor_comments_generated:
                constructor_comments_generated.add(lines[i])
                lines.insert(i, generate_method_comments(author, re.findall(method_param_pattern, lines[i])))
            elif match_destructor_start and lines[i] not in destructor_comments_generated:
                destructor_comments_generated.add(lines[i])
                lines.insert(i, generate_method_comments(author, re.findall(method_param_pattern, lines[i])))
        i += 1
    return lines

def generate_method_comments(method_author: str, parameters: List[str]) -> str:
    method_comments = ""
    method_comments += ("/// @brief Written by: "+method_author+"\n")
    for param in parameters:
        method_comments += ("/// @param "+param[1]+"\n")
        
    method_comments += ("/// @return ")
    return method_comments

def add_method_comments(lines: List[str], author: str) -> List[str]:
    method_comments_generated = set()
    prev_method = ""
    method_start_pattern = r"^\s*(\S+)\s+(\S+)\("
    method_param_pattern = r"([a-zA-Z0-9\*]+)\s+([a-zA-Z0-9\*]+)"
    for i in reversed(range(len(lines))):
        match = re.match(method_start_pattern, lines[i])
        if match and lines[i] != prev_method and match.group(2) not in method_comments_generated:
            prev_method = lines[i]
            method_comments = generate_method_comments(author, re.findall(method_param_pattern, lines[i]))
            lines.insert(i, method_comments)

    return lines

def generate_file_comments(file_name: str, file_author: str) -> str:
    file_comments = ""
    file_comments += ("/// File Name: "+file_name+"\n")
    file_comments += ("/// File Author: "+file_author+"\n")
    file_comments += ("/// Date: "+datetime.today().strftime("%Y-%m-%d")+"\n")
    file_comments += ("/// Description: ")
    
    return file_comments

def remove_previous_comments(lines: List[str]) -> List[str]:
    new_lines = []
    for line in lines:
        if not line.lstrip().startswith("/*") and not line.lstrip().startswith("*") and not line.lstrip().startswith("*/") and not line.lstrip().startswith("///"):
            new_lines.append(line)
    return new_lines

def handle_arguments() -> None:
    parser = argparse.ArgumentParser(description="", usage="python c_comments.py (--file <file_location> | --folder <folder_location>) --author <author>")
    file_folder_group = parser.add_mutually_exclusive_group(required=True)
    file_folder_group.add_argument("--file", dest="file_location", type=str, help="full .h file location that needs to be commented")
    file_folder_group.add_argument("--folder", dest="folder_location", type=str, help="folder containing all .c and .h files that need to be commented")
    parser.add_argument("--author", dest="author", type=str, required=True, help="author of the .h file")

    args = parser.parse_args()
    if args.file_location:
        main(args.file_location, args.author)
    elif args.folder_location:
        if not os.path.isdir(args.folder_location):
            print(f"The specified path '{args.folder_location}' is not a valid directory.")
            return

    for filename in os.listdir(args.folder_location):
        if filename.endswith(".h") or filename.endswith(".c") or filename.endswith(".cpp"):
            file_path = os.path.join(args.folder_location, filename)
            main(file_path, args.author)
    

def main(file_location: str, author: str) -> None:
    file_name, file_extension = os.path.splitext(os.path.basename(file_location))
    with open(file_location, "r") as f:
        lines = [line.rstrip("\n") for line in f]
    lines = remove_previous_comments(lines)
    file_comments = generate_file_comments(file_name, author)
    lines.insert(0, file_comments)
    
    lines = add_class_comments(lines, author)
    
    if file_extension in (".h", ".hpp"):
        lines = add_method_comments(lines, author)

    with open(file_location, "w") as f:
        for line in lines:
            f.write(line + "\n")

if __name__ == "__main__":
    handle_arguments()
