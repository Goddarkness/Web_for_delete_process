
from flask import Flask,render_template,request,redirect
from markupsafe import escape
import psutil
import time

def get_pid(name):
    pids = psutil.process_iter()
    pid_all=[]
    for pid in pids:
        if(pid.name() == name):
            pid_all.append(pid.pid)
    return pid_all

def process_delete(name,running_time):
    pid_all = get_pid(name)
    if (len(pid_all) == 0):
        print( name+' is not in the process')
        return 0
        
    for pid in pid_all:  
        p = psutil.Process(pid)
        if(not p.is_running()):
            print(name+'is not running')
        localtime = time.time()
        if (localtime - p.create_time())>running_time:
            p.kill()

app = Flask(__name__)

@app.route('/',methods = ['POST','GET'])
def index():
    return render_template("base.html")
    


@app.route('/base',methods = ['GET','POST'])
def execute():
    if request.method == 'POST':
        processname = request.form.get('processname')
        runningtime= request.form.get('runningtime')
        process_delete(processname,float(runningtime))
        return "OK"
    else :
        return "NO"
'''    
 
@app.route('/<name>/<float:running_time>')
def index(name,running_time):
    process_delete(name,running_time)
    return "success"
'''
    


app.run(host="0.0.0.0",debug=True,port=5000)