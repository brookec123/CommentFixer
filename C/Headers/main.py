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

def generate_file_comments(file_name, file_author):
    file_comments = ""
    file_comments += ("/// File Name: "+file_name+"\n")
    file_comments += ("/// File Author: "+file_author+"\n")
    file_comments += ("/// Date: "+datetime.today().strftime('%Y-%m-%d')+"\n")
    file_comments += ("/// Description: ")
    
    return file_comments

def main(file_location, author):
    file_name, _ = os.path.splitext(os.path.basename(file_location))
    lines = []
    method_comments_generated = set()
    prev_method = ""
    method_start_pattern = r"^\s*(\w+)\s+(\w+)\s*\("
    method_param_pattern = r"(\w+)\s+(\w+)"

    with open(file_location, "r") as f:
        lines = [line.rstrip('\n') for line in f]
        file_comments = generate_file_comments(file_name, author)
        lines.insert(0, file_comments)
    for i in reversed(range(len(lines))):
        match = re.match(method_start_pattern, lines[i])
        if match and lines[i] != prev_method and match.group(2) not in method_comments_generated:
            prev_method = lines[i]
            method_comments = generate_method_comments(author, re.findall(method_param_pattern, lines[i]))
            lines.insert(i, method_comments)

    with open(file_location, "w") as f:
        for line in lines:
            f.write(line + "\n")

if __name__ == "__main__":
    main(os.path.join(os.getcwd(), "C\\Headers", "tests\\TestFile.h"), "Brooke Cronin")
