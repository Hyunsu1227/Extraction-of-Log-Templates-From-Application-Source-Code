#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess
from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename
import os
import datetime
import threading
import re
import glob
import json


app = Flask(__name__)

# / 요청 시 extract_log_by_source_code.html render
@app.route('/', methods=['GET'])
def extract_log_by_source_code_index():
    return render_template('extract_log_by_source_code.html')


@app.route('/sourcecode', methods=['GET'])
def sourcecode():
    # get 으로 받은 쿼리 인자를 dict 형식으로 받아 data 에 저장
    data = request.args.to_dict()
    java_content = ""
    py_content = ""

    path_dir = './uploadfile/'

    # 쿼리로 filename 인자가 전달 되면
    if 'filename' in data:
        filename = data['filename']
        filename = path_dir + filename

        # 해당 filename을 열어
        fp = open(filename, "r")
        # readlines 함수는 파일의 모든 줄을 읽어서 각각의 줄을 요소로 갖는 리스트로 돌려준다
        # 이를 content 에 할당하고
        if os.path.splitext(filename)[1] == '.py':
            py_content = fp.readlines()
        elif os.path.splitext(filename)[1] == '.java':
            java_content = fp.readlines()
        fp.close()    
        # html 에 전달
        return render_template('sourcecode.html', java_content = java_content, py_content = py_content, title = data['filename'])    
    else :
        # 전달되지 않으면 content 없이 render
        return render_template('sourcecode.html')  

# upload folder 에 file list 를 반환함.
@app.route('/getUploadFileList', methods=['GET'])
def getUploadFileList():
    path_dir = './uploadfile/'

    # file list 읽고 저장 후 정렬
    file_list = os.listdir(path_dir)
    file_list.sort()

    return jsonify(result = "success", result2 = file_list)

@app.route('/upload-file', methods=['POST'])
def uplaod_file():
	# if 'formData' not in request.files:
    # 	return 'File is missing', 404
    files = request.files.getlist('files')
    for file in files:
        print(file)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join("./uploadfile/", filename))
    # for files in request.files.getlist('files') :
    #     print(files)
    #     print(type(files))
    #     if files.filename == '':
    # 	    return 'File is missing', 404
    
    #     filename = files.filename
    #     files.save(os.path.join("./uploadfile/", filename))
    
    return jsonify(result = "success")

@app.route('/excute_extract_log_by_source_code', methods=['post'])
def excute_extract_log_by_source_code():
    # post 로 전달 받은 json 정보를 python dict 형태로 data 에 저장
    data = request.get_json()

    thread_list = []
    print(data)
    if data['extension_type'] == '0':
        command = ['python3', 'lognroll_by_source_code/python/extract_log_py.py', ""]
    if data['extension_type'] == '1':
        command = ['python3', 'lognroll_by_source_code/java/extract_log_java.py', ""]
        
    for filename in data['filename'] :
        if data['extension_type'] == '2':
            if os.path.splitext(filename)[1] == '.py':
                command = ['python3', 'lognroll_by_source_code/python/extract_log_py.py', ""]
            elif os.path.splitext(filename)[1] == '.java':
                command = ['python3', 'lognroll_by_source_code/java/extract_log_java.py', ""]
            
        command[2] = "./uploadfile/"+filename

        t1 = threading.Thread(target=run_process, args=(command,))
        t1.daemon = True
        t1.start()
        thread_list.append(t1)

    for t in thread_list:
        t.join()
    
    concatenate_file()
    success = ""
    with open("lognroll_by_source_code/result/success.txt","r") as f_read:
        success = f_read.read()
    fail = ""
    with open("lognroll_by_source_code/result/fail.txt","r") as f_read:
        fail = f_read.read()
    loglist = ""
    with open("lognroll_by_source_code/result/loglist.txt","r") as f_read:
        loglist = f_read.read()
    
    stat = combine_json_file()
    
    return jsonify(result = "success", result2 = success, result3 = fail, result4 = loglist, result5=stat)

def combine_json_file():
    path = "./lognroll_by_source_code/result/"
    read_files = glob.glob(path + "statistic_*.*")
    stat = {
        'num_log' : 0,
        'success' : 0,
        'fail' : 0,
        'var_only' : 0,
        'string_no_var' : 0,
        'string_var_1' : 0,
        'string_var_over_2' : 0,
        'string_with_e' : 0,
        'classification_failure' : 0,
    }
    print(read_files)

    for f in read_files:
        data = open(f, 'r').read()
        data = json.loads(data)

        stat['num_log'] += data['num_log']
        stat['success'] += data['success']
        stat['fail'] += data['fail']
        stat['var_only'] += data['var_only']
        stat['string_no_var'] += data['string_no_var']
        stat['string_var_1'] += data['string_var_1']
        stat['string_var_over_2'] += data['string_var_over_2']
        stat['string_with_e'] += data['string_with_e']
        stat['classification_failure'] += data['classification_failure']

        if os.path.exists(f):
            os.remove(f)

    return stat

def concatenate_file():
    path = "./lognroll_by_source_code/result/"
    os.chdir(path)

    if os.path.exists("success.txt"):
        os.remove("success.txt")
    else:
        print("The file does not exist")

    read_files = glob.glob("success_*.*")

    print(read_files)
    read_files.sort()

    with open("success.txt", "wb") as outfile:
        for f in read_files:
            i = 0
            filename = f[f.find("_")+1:]
            line = "***********" + filename + "***********" + "\n\n"
            i += 1
            outfile.write(line.encode('utf-8'))
            with open(f, "rb") as infile:
                outfile.write(infile.read())

            if os.path.exists(f):
                os.remove(f)

    if os.path.exists("fail.txt"):
        os.remove("fail.txt")
    else:
        print("The file does not exist")

    read_files = glob.glob("fail_*.*")
    read_files.sort()

    print(read_files)

    with open("fail.txt", "wb") as outfile:
        for f in read_files:
            i = 0
            filename = f[f.find("_")+1:]
            line = "***********" + filename + "***********" + "\n\n"
            i += 1
            outfile.write(line.encode('utf-8'))
            with open(f, "rb") as infile:
                outfile.write(infile.read())
            
            if os.path.exists(f):
                os.remove(f)
    
    if os.path.exists("loglist.txt"):
        os.remove("loglist.txt")
    else:
        print("The file does not exist")

    read_files = glob.glob("loglist_*.*")
    read_files.sort()
    
    print(read_files)

    with open("loglist.txt", "wb") as outfile:
        for f in read_files:
            i = 0
            filename = f[f.find("_")+1:]
            line = "***********" + filename + "***********" + "\n\n"
            i += 1
            outfile.write(line.encode('utf-8'))
            with open(f, "rb") as infile:
                outfile.write(infile.read())
            
            if os.path.exists(f):
                os.remove(f)
    
    os.chdir("../..")

@app.route('/deletefile',methods=['POST'])
def deletefile():
    data=request.get_json()
    filename = data['filename']
    print(filename)
    for i in filename:
        delete_file(i)
    return jsonify(result = "success")

def run_process(command):
    subprocess.run(command)

def delete_file(filename):
    f = "./result/"+filename
    if os.path.isfile(f):
        os.remove(f)
        print(f+" delete success")

    f = "./result-debug/"+filename
    if os.path.isfile(f):
        os.remove(f)
        print(f+" delete success")

    f = "./uploadfile/"+filename
    if os.path.isfile(f):
        os.remove(f)
        print(f+" delete success")
    
# log.log file을 함수 호출 시 확인하여 '!--\n' marking이 확인 되면
# 이전 마킹부터 해당 마킹까지 새로운 파일에 저장함. 

if __name__ == '__main__':
    global f
    listen_port = '4001'

    # ipaddr=subprocess.getoutput("hostname -I").split()[0]
    # print ("Starting the service with ip_addr="+ipaddr)

    app.run(debug=True,host='127.0.0.1',port=int(listen_port),threaded=True)
    f.close()

