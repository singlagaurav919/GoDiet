from flask import Flask, render_template, request,redirect, url_for
from werkzeug import secure_filename
import cloudsight
from nutritionix import Nutritionix

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app = Flask(__name__)

auth = cloudsight.SimpleAuth('uquMfLmzXYvnSwR6g52zFA')
api = cloudsight.API(auth)

nix = Nutritionix(app_id="29a3ea8f", api_key="f04d3ef0949ad6d732ee4397afe6f374")

@app.route('/index.html')
def home():
    return redirect(url_for('hello_world'))

@app.route('/calo/index.html')
def home_table():
    return redirect(url_for('hello_world'))

@app.route('/about.html')
def about():
    return render_template("about.html")

@app.route('/contact.html')
def contact():
    return render_template("contact.html")

global file
global link
global route

@app.route('/calo')
def calorie_count():
    if route==True:
        global file
        print file
        with open(file, 'rb') as f:
            response = api.image_request(f, 'your-file.jpg', {
                'image_request[locale]': 'en-US',
            })
    else:
        global link
        response = api.remote_image_request(link ,{
            'image_request[locale]': 'en-US',
        })
    status = api.image_response(response['token'])
    print status
    if status['status'] != cloudsight.STATUS_NOT_COMPLETED:
        # Done!
        pass
    status = api.wait(response['token'], timeout=60)
    result = nix.search(status["name"], results="0:1").json()["hits"][0]["fields"]["item_id"]
    result = nix.search(status["name"], results="0:1").json()["hits"][0]["fields"]["item_id"]
    result = nix.item(id=result).json()
    updated_list = dict()
    with open("list.txt", "r") as filestream:
        for line in filestream:
            currentline = line.split(",")
            updated_list[currentline[0]] = result[currentline[1][:-1]]
    return render_template("pretty.html", result=updated_list)
    #return '%s' %result
	
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    global file
    global route
    route=True
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
    #return 'file uploaded successfully'
        file = f.filename
	return redirect(url_for('calorie_count'))

@app.route('/upload_link', methods = ['GET', 'POST'])
def upload_link():
    if request.method == 'POST':
        global route
        route = False
        global link
        link = request.form['text']
        print link
	return redirect(url_for('calorie_count'))

@app.route('/')
def hello_world():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug = False,port=80)