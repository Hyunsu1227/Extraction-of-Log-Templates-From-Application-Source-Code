from join_line_py import join_line
from organize_log import organize_log
from grep import grep
from trim import trim_line
import sys
import os

if __name__ == "__main__":
    filename = os.path.basename(sys.argv[1])

    path = "./lognroll_by_source_code/result/"
    join_line(sys.argv[1], path + "a_" + filename)
    grep(path + "a_" + filename,  path + "b_" + filename)
    trim_line(path + "b_" + filename, path + "c_" + filename)
    organize_log(path + "c_" + filename, path + "success_" + filename, path + "fail_" + filename, path + "statistic_" + filename, path + "loglist_" + filename)

    if os.path.isfile(path + "a_" + filename):
        os.remove(path + "a_" + filename)
    if os.path.isfile(path + "b_" + filename):
        os.remove(path + "b_" + filename)
    if os.path.isfile(path + "c_" + filename):
        os.remove(path + "c_" + filename)    