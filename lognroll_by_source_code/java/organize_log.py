import json
import re

def organize_log(before_file, logtemplate_file_suc, logtemplate_file_fail, statisitc_json, print_loglist_file):
    fin = open(before_file,"r")
    fout = open(print_loglist_file,"w")
    fout2 = open(logtemplate_file_fail,"w")

    var_only = [] # LOG.warn(errMsg);
    string_with_e = [] # LOG.warn("failed to generate key", e);
    string_no_var = [] # LOG.trace("Entering createKey Method.");
    string_var_1 = [] # LOG.info("Elapsed Time: " + getElapsedTime()); or LOG.trace("SPNEGO completed for client principal [{}]",clientPrincipal);
    string_var_over_2 = [] # LOG.info("Using keytab {}, for principal {}",keytab, krbPrincipal);
    classification_failure = []

    while True:
        line = fin.readline()

        if not line: 
            break
        
        quotes_cnt = line.count('"')
        plus_cnt = line.count("+")

        i = 0
        quotes_outside = ""
        quotes_inside = ""
        for piece in line.split('"'):
            if i % 2 == 0 :
                quotes_outside += piece + ' '
            else :
                quotes_inside += piece + ' '
            i += 1
        brace_cnt = quotes_inside.count("{}")
        rest_cnt = quotes_outside.count(",")
        

        if (brace_cnt == 0 and plus_cnt - quotes_cnt/2 + 1 == 0) and brace_cnt == rest_cnt and quotes_cnt > 0:
            string_no_var.append(line)
        elif (brace_cnt == 1 or plus_cnt - quotes_cnt/2 + 1 == 1) and brace_cnt == rest_cnt and quotes_cnt > 0:
            string_var_1.append(line)
        elif (brace_cnt >= 2 or plus_cnt - quotes_cnt/2 + 1 >= 2) and brace_cnt == rest_cnt and quotes_cnt > 0:
            string_var_over_2.append(line)
        elif brace_cnt < rest_cnt:
            string_with_e.append(line)
        elif brace_cnt + rest_cnt + quotes_cnt == 0 and \
            (line.find("LOG.debug") != -1 or line.find("LOG.info") != -1 or line.find("LOG.trace") != -1 or line.find("LOG.error") != -1 or line.find("LOG.warn") != -1) :
            var_only.append(line)
        elif (line.find("LOG.debug") != -1 or line.find("LOG.info") != -1 or line.find("LOG.trace") != -1 or line.find("LOG.error") != -1 or line.find("LOG.warn") != -1):
            classification_failure.append(line)
        
    stat = {
        'num_log' : len(var_only) + len(string_with_e) + len(classification_failure) + len(string_no_var) + len(string_var_1) + len(string_var_over_2),
        'success' : len(string_no_var) + len(string_var_1) + len(string_var_over_2),
        'fail' : len(var_only) + len(string_with_e) + len(classification_failure),
        'var_only' : len(var_only),
        'string_no_var' : len(string_no_var),
        'string_var_1' : len(string_var_1),
        'string_var_over_2' : len(string_var_over_2),
        'string_with_e' : len(string_with_e),
        'classification_failure' : len(classification_failure),
    }

    with open(statisitc_json, 'w') as f:
        json.dump(stat, f)
        
    for line in var_only:
        # fout.write(line)
        fout2.write(line)
    
    # fout.write('-------------------------------------------------------------------------\n')
    # fout.write('-!-----------------------------------------------------------------------\n')
    # fout.write('-------------------------------------------------------------------------\n')

    for line in string_no_var:
        fout.write(line)

    # fout.write('-------------------------------------------------------------------------\n')
    # fout.write('-!-----------------------------------------------------------------------\n')
    # fout.write('-------------------------------------------------------------------------\n')
    
    for line in string_var_1:
        fout.write(line)

    # fout.write('-------------------------------------------------------------------------\n')
    # fout.write('-!-----------------------------------------------------------------------\n')
    # fout.write('-------------------------------------------------------------------------\n')
    
    for line in string_var_over_2:
        fout.write(line)

    # fout.write('-------------------------------------------------------------------------\n')
    # fout.write('-!-----------------------------------------------------------------------\n')
    # fout.write('-------------------------------------------------------------------------\n')

    for line in string_with_e:
        # fout.write(line)
        fout2.write(line)

    # fout.write('-------------------------------------------------------------------------\n')
    # fout.write('-!-----------------------------------------------------------------------\n')
    # fout.write('-------------------------------------------------------------------------\n')

    for line in classification_failure:
        # fout.write(line)
        fout2.write(line)

    extract_log_string_no_var(string_no_var=string_no_var, after_file=logtemplate_file_suc)

    extract_log_string_var(string_var= string_var_1 + string_var_over_2, after_file=logtemplate_file_suc)
        
    fin.close()
    fout.close()

def extract_log_string_no_var(string_no_var, after_file):
    f = open(after_file , "w")
   
    quotes_inside = ""
    i = 0
    for line in string_no_var:
        if line[line.find('(') + 1] == '"' or line[line.find('(') + 1] == "'":
            for piece in line.split(line[line.find('(') + 1]):
                if i % 2 == 1 :
                    quotes_inside += piece + ' '
                i += 1
            i = 0
            quotes_inside += '\n'
            f.write(quotes_inside)
            quotes_inside = ""

    f.close()

def extract_log_string_var(string_var, after_file):
    f = open(after_file , "a")
   
    quotes_inside = ""
    i = 0
    for line in string_var:
        if line[line.find('(') + 1] == '"' or line[line.find('(') + 1] == "'":
            for piece in line.split(line[line.find('(') + 1]):
                if i % 2 == 1 :
                    quotes_inside += piece + ' '
                else :
                    if piece.count("+") >= 2 or piece.count("+") + piece.count(";") >= 2:
                        quotes_inside += "*"
                    if piece.find(",") != -1:
                        break
                i += 1
            i = 0
            quotes_inside += '\n'

            quotes_inside = re.sub('[{][]}]',"*", quotes_inside)
            
            f.write(quotes_inside)
            quotes_inside = ""

    f.close()

if __name__ == "__main__":
    organize_log("hadoopLog", "hadoopLog_organize")