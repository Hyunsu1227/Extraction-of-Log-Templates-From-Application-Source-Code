import time

dir = '../result/'
filename = dir + "log.log"

f = open(filename, "w")

def print_web(*args):    
    sentence = "".join(map(str,args)) + '\n'
    # sentence = sentence.replace('"', '\\"')
    f.write(sentence)
    f.flush()

for i in range(0,5):
    print_web(i)
    time.sleep(1)

print_web("!--")

for i in range(5,10):
    print_web(i)
    time.sleep(1)

print_web("!--")

for i in range(10,15):
    print_web(i)
    time.sleep(1)

print_web("!--")