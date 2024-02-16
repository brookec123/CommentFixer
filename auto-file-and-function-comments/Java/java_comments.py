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
        for i in range(len(lines)):
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
                if "{" in lines[i]:
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
                           
    with open(file_location, "w") as f:              
        for i in lines:
            f.write(str(i))

if __name__ == "__main__":
    handle_arguments()