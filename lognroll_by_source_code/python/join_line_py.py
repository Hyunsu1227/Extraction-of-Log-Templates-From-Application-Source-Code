
def combine_into_one_line(line, left, right, fin):
    if line.find(left) != -1 and line[-2] != right:
        # print(line)
        line = line.rstrip()
        while True :
            string = fin.readline()
            # print(string)
            line += string.strip()
            try:
                if string[-2] == ')':
                    break
            except:
                print(line)
        line+='\n'
    return line

def join_line(before_file, after_file):
    # fin = open("../pythonfile/manager.py","r")
    # fout = open("result/manager.py","w")
    fin = open(before_file,"r")
    fout = open(after_file,"w")

    while True:
        line = fin.readline()
        line = combine_into_one_line(line,"LOG.warning(", ")", fin)
        line = combine_into_one_line(line,"LOG.debug(", ")", fin)
        line = combine_into_one_line(line,"LOG.info(", ")", fin)
        line = combine_into_one_line(line,"LOG.error(", ")", fin)
        line = combine_into_one_line(line,"LOG.exception(", ")", fin)
        
        fout.write(line)

        if not line: 
            break
        
    fin.close()
    fout.close()

if __name__ == "__main__":
    #join_line("../pythonfile/manager.py", "result/manager.py")
    join_line("ironic_all", "ironic_join")