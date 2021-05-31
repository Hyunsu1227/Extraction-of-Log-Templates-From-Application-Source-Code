import re

def grep(before_file, after_file):
    fin = open(before_file,"r")
    fout = open(after_file,"w")
    
    pattern = "LOG[.]"

    for line in fin:
        if re.search(pattern, line):
            fout.write(line)
        
    fin.close()
    fout.close()

if __name__ == "__main__":
    
    grep("ironic_join", "grep")