import argparse
import os
import regex as re
from typing import List
from datetime import datetime

def generate_method_comments(method_author: str, parameters: List[str], return_value: str, additional_method_comments: List[str]) -> str:
    method_comments = "    \"\"\"\n"
    method_comments += ("    Description: Written by: "+method_author+"\n")
    for comment in additional_method_comments:
        method_comments += ("    " + comment + "\n")
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

def get_params(line: str) -> List[str]:
    lst = re.findall(r"(([_a-zA-Z0-9\*]+)\s*:\s*([_a-zA-Z0-9\*]+))*", line)
    lst = [x for x in lst if not x == ('', '', '')]
    if len(lst) == 0:
        return ["Not Specified"]
    return lst

def add_method_comments(lines: List[str], author: str, additional_method_comments: List[str]) -> List[str]:
    method_start_pattern = r"^\s*def\s+([_a-zA-Z0-9\*]+)\s*\("
    method_end_pattern = r"->\s*([a-z]+):"
    i = 0
    while i < len(lines):
        match1 = re.match(method_start_pattern, lines[i])
        match2 = re.findall(method_end_pattern, lines[i])
        if match1:
            if match2:
                method_comments = generate_method_comments(author, get_params(lines[i]), match2[0], additional_method_comments)
                lines.insert(i+1, method_comments)
            else:
                method_comments = generate_method_comments(author, get_params(lines[i]), "Not Specified", additional_method_comments)
                lines.insert(i+1, method_comments)
        i = i+1
    return lines

def generate_file_comments(file_name: str, file_author: str, include_date: bool, additional_file_comments: List[str]) -> str:
    file_comments = "\"\"\"\n"
    file_comments += ("File Name: "+file_name+"\n")
    file_comments += ("File Author: "+file_author+"\n")
    if include_date:
        file_comments += ("Date: "+datetime.today().strftime("%Y-%m-%d")+"\n")
    for comment in additional_file_comments:
        file_comments += (comment + "\n")
    file_comments += ("Description: ")
    file_comments += "\n\"\"\""
    return file_comments

def remove_previous_comments(lines: List[str]) -> List[str]:
    new_lines = []
    insideComment = False
    for line in lines:
        if line.lstrip().startswith("\'\'\'") or line.lstrip().startswith("\"\"\""):
            insideComment = not insideComment
        elif not insideComment and not line.lstrip().startswith("#"):
            new_lines.append(line)
    return new_lines

def create_additional_comment_list(comments: str) -> List[str]:
    return comments.split("\\~\\`/~/")

def handle_arguments() -> None:
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
    with open(file_location, "r") as f:
        lines = [line.rstrip("\n") for line in f]
    lines = remove_previous_comments(lines)
    file_comments = generate_file_comments(file_name, author, include_date, additional_file_comments)
    lines.insert(0, file_comments)
    lines = add_method_comments(lines, author, additional_method_comments)

    with open(file_location, "w") as f:
        for line in lines:
            f.write(line + "\n")

if __name__ == "__main__":
    handle_arguments()
