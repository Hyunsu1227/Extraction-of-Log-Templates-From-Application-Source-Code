import subprocess
import threading
import time


def run_process(command):
    subprocess.run(command)

command = ['python3', '../lognroll/32_tree_and_SLCL_py3_print_web.py', '--linear' , '--logfile', '../lognroll/log_sample/cassandra_10k.log']
# debug_mode == True 면 command 에 추가
    
# if data['debug_mode'] == 'True' :
#     command.append('--debug')
#     filename += 'debug'

command.append('--filename')
command.append('../result/'+'filename')
# 해당 커맨드 실행 -> 이후 스레드 형식으로 구현할 예정

t1 = threading.Thread(target=run_process, args=(command,))
t1.daemon = True
t1.start()


time.sleep(20)