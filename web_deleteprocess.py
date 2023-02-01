
from flask import Flask,render_template,request,redirect,session
from markupsafe import escape
import psutil
import time
from time import sleep
import functools







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
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/',methods = ['POST','GET'])
def index():
    user = session.get('username')
    if  user:
        return render_template("base.html")
    return render_template("login.html")
    


@app.route('/login',methods=['POST','GET'] )

def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')   
    password = request.form.get('password')
 
    if username =='hjy' and password =='123':
        session['username'] = username
        return render_template('base.html')
    return render_template('login.html')
   
def is_login(func):
    @functools.wraps(func)
    def inner(*args,**kwargs):
        user = session.get('username')
        if not user:
             return redirect('/login')
        return func(*args,**kwargs)
    return inner


@app.route('/base',methods = ['GET','POST'])
@is_login
def execute():
    if request.method == 'POST':
        processname = request.form.get('processname')
        runningtime= request.form.get('runningtime')
        process_delete(processname,float(runningtime))
        return render_template("OK.html")
    else :
        return render_template("NO.html")




''' 
@app.route('/<name>/<float:running_time>')
def index(name,running_time):
    process_delete(name,running_time)
    return "success"
'''
    


app.run(host="0.0.0.0",debug=True,port=5000)