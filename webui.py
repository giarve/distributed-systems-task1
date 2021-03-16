from flask import Flask, render_template, request, redirect, flash

ALLOWED_UPLOAD_EXTENSIONS = {'py'}

app = Flask(__name__)

def webui_serve():
    app.run(host='0.0.0.0', port=8080)

worker_info = {
    "0": "Running",
    "1": "Idle",
    "2": "Idle"
}

@app.route('/')
def index():
    return render_template('index.html', workers=worker_info)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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
            print(file)

            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/index')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''