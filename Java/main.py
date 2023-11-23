import os
import regex as re
from datetime import datetime

def generate_method_comments(method_name, method_author, return_type, parameters):
    method_comments = ""
    method_comments += ("/*"+"\n")
    method_comments += (" * Method Name: "+method_name+"\n")
    method_comments += (" * Method Author: "+method_author+"\n")
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

def generate_file_comments(file_name, file_author):
    file_comments = ""
    file_comments += ("/*"+"\n")
    file_comments += (" * File Name: "+file_name+"\n")
    file_comments += (" * File Author: "+file_author+"\n")
    file_comments += (" * Date: "+datetime.today().strftime('%Y-%m-%d')+"\n")
    file_comments += (" * Description: "+"\n")
    file_comments += (" */"+"\n\n")
    
    return file_comments

def main(file_location, file_name):
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
                    file_comments = generate_file_comments(file_name, "Brooke Cronin")
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
                    print(method_line)
                    match = re.match(method_start_pattern, method_line)
                    if match:
                        method_comments = generate_method_comments(match.group(2), "Brooke Cronin", match.group(1), re.findall(method_param_pattern, lines[i]))
                        method_comments_generated = True
                        lines.insert(i, method_comments)
                           
    with open(file_location, "w") as f:              
        for i in lines:
            f.write(str(i))

if __name__ == "__main__":
    main(os.path.join(os.getcwd(), "Java", "tests\\TestFile.java"), "TestFile")