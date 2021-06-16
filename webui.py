from flask import Flask, render_template, request, redirect, flash

from google.protobuf import empty_pb2
import server_pb2
import types
import dill as pickle
from datetime import datetime


ALLOWED_UPLOAD_EXTENSIONS = {'py'}

app = Flask(__name__)

def import_code(code):
    # create blank module
    module = types.ModuleType("tmp")
    # populate the module with code
    exec(code, module.__dict__)
    return module

def webui_serve(server_connection):
    app.config['sv_conn'] = server_connection
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(host='0.0.0.0', port=8080)

@app.route('/')
def index():
    worker_info = app.config['sv_conn'].server_workmgmt_stub_singleton.list(empty_pb2.Empty()).workers
    worker_info.sort(key=lambda x: x.id)
    job_info = app.config['sv_conn'].server_jobmgmt_stub_singleton.list(empty_pb2.Empty()).jobs
    new_jobs = []

    for job in job_info:
        new_job = {}
        new_job['id'] = job.id
        new_job['ended_at'] = datetime.fromtimestamp(job.ended_at.ToSeconds())
        new_job['result'] = job.result
        new_jobs.append(new_job)

    new_jobs.sort(key=lambda x: x['ended_at'], reverse=True)

    return render_template('index.html', workers=worker_info, jobs=new_jobs)

@app.route('/worker/create', methods=['POST'])
def createWorker():
    print(request.form)

    numWorkers = int(request.form['numWorkers'])

    app.config['sv_conn'].server_workmgmt_stub_singleton.create(server_pb2.NumberOfWorkers(num=numWorkers))
    return redirect('/')

@app.route('/worker/delete/<int:workerId>', methods=['GET'])
def deleteWorker(workerId):
    app.config['sv_conn'].server_workmgmt_stub_singleton.delete(server_pb2.WorkerId(id=workerId))
    return redirect('/')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        contents = file.read().decode('utf-8')
        module = import_code(contents)

        map_func = getattr(module, "map_func", None)
        reduce_func = getattr(module, "reduce_func", None)

        if map_func is None:
            flash('No map function')

        if not request.form['args']:
            flash("At least one argument is required")

        args = request.form['args'].split(' ')

        if reduce_func is None and len(args) > 1:
            flash('More than 1 argument, reduce function is required')

        map_function_pickled = pickle.dumps(map_func)
        reduce_function_pickled = pickle.dumps(reduce_func)
        app.config['sv_conn'].server_jobmgmt_stub_singleton.create(server_pb2.WorkType(map_function_pickled=map_function_pickled, reduce_function_pickled=reduce_function_pickled, args=args))

        return redirect('/')
