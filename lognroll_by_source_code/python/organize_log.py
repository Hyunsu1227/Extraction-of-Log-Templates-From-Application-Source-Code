import re
import json

def organize_log(before_file, logtemplate_file_suc, logtemplate_file_fail, statisitc_json, print_loglist_file):
    fin = open(before_file,"r")
    fout = open(logtemplate_file_fail,"w")
    fout2 = open(print_loglist_file,"w")

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
        
        i = 0
        quotes_cnt = 0
        quotes_outside = ""
        quotes_inside = ""
        if line[line.find('(') + 1] == '"' or line[line.find('(') + 1] == "'":
            line = line.replace("\\\"","'")
            line = line.replace('\\\'','"')
            for piece in line.split(line[line.find('(') + 1]):
                if i % 2 == 0 :
                    quotes_outside += piece + ' '
                else :
                    quotes_inside += piece + ' '
                i += 1
            quotes_cnt = line.count(line[line.find('(') + 1])
        else :
            quotes_outside = line

        format_cnt = quotes_inside.count("%s") + quotes_inside.count("%d") + quotes_inside.count("%i") +quotes_inside.count("%r")
        rest_cnt = quotes_outside.count(",")
        percent_paren_cnt = quotes_inside.count("%(")
        equal_cnt = quotes_outside.count("=")

        if line[:4] == 'LOG.':
            if format_cnt + quotes_cnt== 0 and equal_cnt == 0:
                var_only.append(line)
            elif rest_cnt + format_cnt +percent_paren_cnt == 0 and quotes_cnt > 0 :
                string_no_var.append(line)
            elif (format_cnt + percent_paren_cnt == 1)and equal_cnt == 0:
                string_var_1.append(line)
            elif format_cnt + percent_paren_cnt >= 2 and equal_cnt == 0:
                string_var_over_2.append(line)    
            elif equal_cnt > 0:
                string_with_e.append(line)
            else :
                classification_failure.append(line)
                # print(line)

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
        fout.write(line)
        
    
    # fout.write('-------------------------------------------------------------------------\n')
    # fout.write('-!-----------------------------------------------------------------------\n')
    # fout.write('-------------------------------------------------------------------------\n')

    for line in string_no_var:
        fout2.write(line)

    # fout.write('-------------------------------------------------------------------------\n')
    # fout.write('-!-----------------------------------------------------------------------\n')
    # fout.write('-------------------------------------------------------------------------\n')
    
    for line in string_var_1:
        fout2.write(line)

    # fout.write('-------------------------------------------------------------------------\n')
    # fout.write('-!-----------------------------------------------------------------------\n')
    # fout.write('-------------------------------------------------------------------------\n')
    
    for line in string_var_over_2:
        fout2.write(line)

    # fout.write('-------------------------------------------------------------------------\n')
    # fout.write('-!-----------------------------------------------------------------------\n')
    # fout.write('-------------------------------------------------------------------------\n')

    for line in string_with_e:
        fout.write(line)
        

    # fout.write('-------------------------------------------------------------------------\n')
    # fout.write('-!-----------------------------------------------------------------------\n')
    # fout.write('-------------------------------------------------------------------------\n')

    for line in classification_failure:
        fout.write(line)
        

    extract_log_string_no_var(string_no_var=string_no_var, after_file=logtemplate_file_suc)

    extract_log_string_var(string_var= string_var_1 + string_var_over_2, after_file=logtemplate_file_suc)

    fin.close()
    fout.close()
    fout2.close()

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
                    if piece.find(",") != -1:
                        break
                i += 1
            i = 0
            quotes_inside += '\n'

            quotes_inside = re.sub('%s',"*", quotes_inside)
            quotes_inside = re.sub('%r',"*", quotes_inside)
            quotes_inside = re.sub('%d',"*", quotes_inside)
            quotes_inside = re.sub('%f',"*", quotes_inside)
            quotes_inside = re.sub(r'[%][(][a-zA-Z0-9_-]+[)][s]',"*", quotes_inside)
            quotes_inside = re.sub(r'[%][(][a-zA-Z0-9_]+[)][d]',"*", quotes_inside)
            quotes_inside = re.sub(r'[%][(][a-zA-Z0-9_]+[)][r]',"*", quotes_inside)
            quotes_inside = re.sub(r'[%][(][a-zA-Z0-9_]+[)][.0-9]+[f]',"*", quotes_inside)

            f.write(quotes_inside)
            quotes_inside = ""

    f.close()

if __name__ == "__main__":
    organize_log("ironicLog", "ironicLog_templ", "ironicLog_fail_list")