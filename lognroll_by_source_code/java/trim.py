

# def trim_line(before_file, after_file):
    
#     fin = open(before_file,"r")
#     fout = open(after_file,"w")

#     while True:
#         line = fin.readline()
        
#         if line.find("hadoop_all_java_join:") != -1 :
#             line = line[22:]
#             line = line.strip()
#             line += '\n'
#             fout.write(line)

#         if not line: 
#             break
        
#     fin.close()
#     fout.close()

def trim_line(before_file, after_file):
    
    fin = open(before_file,"r")
    fout = open(after_file,"w")

    i=0
    while True:
        line = fin.readline()
        
        if not line: 
            break
        
        line = line.strip()
        line += '\n'
        fout.write(line)
        
        i+=1
        
        
    fin.close()
    fout.close()

if __name__ == "__main__":
    #join_line("../pythonfile/manager.py", "result/manager.py")
    trim_line("hadoop_all_java_join_before_trim", "hadoopLog")