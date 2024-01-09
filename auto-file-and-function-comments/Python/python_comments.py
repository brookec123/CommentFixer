import argparse
import os
import regex as re
from datetime import datetime

def generate_method_comments(method_author, parameters, return_value):
    method_comments = "    \"\"\"\n"
    method_comments += ("    Description: Written by: "+method_author+"\n")
    method_comments += ("    ### Parameters\n")
    if parameters == ["Not Specified"]:
        method_comments += ("    - Not Specified\n")
    else:
        for param in parameters:
            method_comments += ("    - "+param[1]+":"+param[2]+"\n")
    method_comments += ("    ### Returns\n")
    method_comments += ("    - "+return_value+"\n")
    method_comments += "    \"\"\"\n"
    return method_comments

def get_params(line):
    lst = re.findall(r"(([a-z]+)\s*:\s*([a-z]+))*", line)
    lst = [x for x in lst if not x == ('', '', '')]
    if len(lst) == 0:
        return ["Not Specified"]
    return lst

def add_method_comments(lines, author):
    method_start_pattern = r"^\s*def\s+([a-zA-Z0-9\*]+)\s*\("
    method_end_pattern = r"->\s*([a-z]+):"
    i = 0
    while i < len(lines):
        match1 = re.match(method_start_pattern, lines[i])
        match2 = re.findall(method_end_pattern, lines[i])
        if match1:
            if match2:
                method_comments = generate_method_comments(author, get_params(lines[i]), match2[0])
                lines.insert(i+1, method_comments)
            else:
                method_comments = generate_method_comments(author, get_params(lines[i]), "Not Specified")
                lines.insert(i+1, method_comments)
        i = i+1
    return lines

def generate_file_comments(file_name, file_author):
    file_comments = "\"\"\"\n"
    file_comments += ("File Name: "+file_name+"\n")
    file_comments += ("File Author: "+file_author+"\n")
    file_comments += ("Date: "+datetime.today().strftime("%Y-%m-%d")+"\n")
    file_comments += ("Description: ")
    file_comments += "\n\"\"\""
    
    return file_comments

def remove_previous_comments(lines):
    new_lines = []
    insideComment = False
    for line in lines:
        if line.lstrip().startswith("\'\'\'") or line.lstrip().startswith("\"\"\""):
            insideComment = not insideComment
        elif not insideComment and not line.lstrip().startswith("#"):
            new_lines.append(line)
    return new_lines

def handle_arguments():
    parser = argparse.ArgumentParser(description="", usage="python java_comments.py (--file <file_location> | --folder <folder_location>) --author <author>")
    file_folder_group = parser.add_mutually_exclusive_group(required=True)
    file_folder_group.add_argument("--file", dest="file_location", type=str, help="full .java file location that needs to be commented")
    file_folder_group.add_argument("--folder", dest="folder_location", type=str, help="folder containing all .java files that need to be commented")
    parser.add_argument("--author", dest="author", type=str, required=True, help="author of the .h file")

    args = parser.parse_args()
    if args.file_location:
        main(args.file_location, args.author)
    elif args.folder_location:
        if not os.path.isdir(args.folder_location):
            print(f"The specified path '{args.folder_location}' is not a valid directory.")
            return

def main(file_location, author):
    file_name, _ = os.path.splitext(os.path.basename(file_location))
    with open(file_location, "r") as f:
        lines = [line.rstrip("\n") for line in f]
    lines = remove_previous_comments(lines)
    file_comments = generate_file_comments(file_name, author)
    lines.insert(0, file_comments)
    lines = add_method_comments(lines, author)

    with open(file_location, "w") as f:
        for line in lines:
            f.write(line + "\n")

if __name__ == "__main__":
    handle_arguments()
