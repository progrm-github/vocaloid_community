from flask import Flask, render_template, request, redirect
import sqlite3
from random import *
from flask import request
import os
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename
from flask import send_file
import glob
import random

db = sqlite3.connect("db.db",check_same_thread=False)
cur = db.cursor()

app = Flask(__name__)
dropzone = Dropzone(app)
global int1
int1 = 0
@app.route('/')
def index():
    sql = "SELECT * from userdata"
    cur.execute(sql)

    data_list = cur.fetchall()

    path_dir = './image'

    file_list = os.listdir(path_dir)
    fileEx = r'.png'
    file_list = [file for file in os.listdir(path_dir) if file.endswith(fileEx)]


    random.shuffle(file_list)


    return render_template('main.html', value=data_list, imagelink=request.host_url + 'image/' + file_list[0], imagelink1=request.host_url + 'image/' + file_list[1], imagelink2=request.host_url + 'image/' + file_list[2], imagelink3=request.host_url + 'image/' + file_list[3], imagelink4=request.host_url + 'image/' + file_list[4])


@app.route('/admin')
def indexadmin():
    sql = "SELECT * from userdata"
    cur.execute(sql)

    data_list = cur.fetchall()

    path_dir = './image'

    file_list = os.listdir(path_dir)
    fileEx = r'.png'
    file_list = [file for file in os.listdir(path_dir) if file.endswith(fileEx)]


    random.shuffle(file_list)


    return render_template('admin.html', value=data_list, imagelink=request.host_url + 'image/' + file_list[0], imagelink1=request.host_url + 'image/' + file_list[1], imagelink2=request.host_url + 'image/' + file_list[2], imagelink3=request.host_url + 'image/' + file_list[3], imagelink4=request.host_url + 'image/' + file_list[4])


@app.route('/write')
def write():
    return render_template('write.html')
@app.route('/use')
def use():
    return render_template("use.html")
@app.route('/fileupload', methods=['POST'])
def file_upload():
    file = request.files['file']

    filename = secure_filename(file.filename)
    file.save(os.path.join('./image', filename))
    files = glob.glob("./image/*.*")
    for x in files:
        if not os.path.isdir(x):
            filename = os.path.splitext(x)
            try:
                os.rename(x,filename[0] + '.png')
            except:
                pass
    return redirect('/')
@app.route('/notice')
def notice():
    return render_template("notice.html")
@app.route('/image/<name>')
def pyoshi(name):
    return send_file('./image/' + name, attachment_filename=name)
@app.route('/imgupload')
def upimg():
    return render_template('upimage.html')
@app.route('/loding',methods=['GET', 'POST'])
def roding():
    global int1
    name = request.args.get('name')
    title = request.args.get('title')
    result = request.args.get('result')
    print(result)
    sql = "SELECT * from userdata"
    cur.execute(sql)


    mycursor = db.cursor()
    c = randrange(999999)

    sql = "INSERT INTO userdata ('num', 'title', 'writer', 'views', 'context') VALUES (?,?,?,?,?)"
    val = (str(c), str(title), str(name), '1', str(result))

    mycursor.execute(sql, val)

    db.commit()
    return redirect('/')
@app.route('/look/<int:articleID>/')
def board_content(articleID):
    UserId = articleID

    sql = "SELECT * FROM userdata WHERE num = '{}'".format(UserId)

    cur.execute(sql)

    result = cur.fetchall()


    sql1= "UPDATE userdata SET views = views + 1 WHERE num='{}'".format(UserId)

    cur.execute(sql1)

    return render_template("look.html", result=result)

@app.errorhandler(404)
def page_not_found(error):
     return redirect(request.host_url)

@app.route('/main.html')
def gomain():
    return redirect(request.host_url)

@app.route('/delete/<id>')
def delete(id):
    sql = "DELETE FROM userdata WHERE num = {}".format(id)

    cur.execute(sql)

    db.commit()
    return redirect(request.host_url)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
