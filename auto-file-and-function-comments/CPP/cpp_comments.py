import argparse
import os
import regex as re
from datetime import datetime

def generate_method_comments(method_author, parameters):
    method_comments = ""
    method_comments += ("/// @brief Written by: "+method_author+"\n")
    parameters.pop(0)
    for param in parameters:
        method_comments += ("/// @param "+param[1]+"\n")
        
    method_comments += ("/// @return ")
    return method_comments

def add_class_comments(lines, author):
    pass

def add_method_comments(lines, author):
    method_comments_generated = set()
    prev_method = ""
    method_start_pattern = r"^\s*([a-zA-Z0-9\*]+)\s+([a-zA-Z0-9\*]+)\s*\("
    method_param_pattern = r"([a-zA-Z0-9\*]+)\s+([a-zA-Z0-9\*]+)"
    for i in reversed(range(len(lines))):
        match = re.match(method_start_pattern, lines[i])
        if match and lines[i] != prev_method and match.group(2) not in method_comments_generated:
            prev_method = lines[i]
            method_comments = generate_method_comments(author, re.findall(method_param_pattern, lines[i]))
            lines.insert(i, method_comments)
    return lines

def generate_file_comments(file_name, file_author):
    file_comments = ""
    file_comments += ("/// File Name: "+file_name+"\n")
    file_comments += ("/// File Author: "+file_author+"\n")
    file_comments += ("/// Date: "+datetime.today().strftime("%Y-%m-%d")+"\n")
    file_comments += ("/// Description: ")
    
    return file_comments

def remove_previous_comments(lines):
    new_lines = []
    for line in lines:
        if not line.lstrip().startswith("/*") and not line.lstrip().startswith("*") and not line.lstrip().startswith("*/") and not line.lstrip().startswith("///"):
            new_lines.append(line)
    return new_lines

def handle_arguments():
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
        if filename.endswith(".h") or filename.endswith(".hpp") or filename.endswith(".cpp"):
            file_path = os.path.join(args.folder_location, filename)
            main(file_path, args.author)
    

def main(file_location, author):
    file_name, file_extension = os.path.splitext(os.path.basename(file_location))
    with open(file_location, "r") as f:
        lines = [line.rstrip("\n") for line in f]
    lines = remove_previous_comments(lines)
    file_comments = generate_file_comments(file_name, author)
    lines.insert(0, file_comments)
    
    if file_extension == ".h" or file_extension == ".hpp":
        lines = add_method_comments(lines, author)

    with open(file_location, "w") as f:
        for line in lines:
            f.write(line + "\n")

if __name__ == "__main__":
    handle_arguments()
