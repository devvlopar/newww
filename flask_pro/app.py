from flask import Flask, render_template, request, flash
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.secret_key = 'wertyui'
app.config['UPLOAD_FOLDER'] = 'static/profile_photos/'
app.config['MYSQL_USER'] = 'dev'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'testdb'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'GET':
        return render_template('upload_image.html')
    print(request.files)
    if 'profile_pic' not in request.files:
        flash('no image selected!!')
        return render_template('upload_image.html', message='no image was selected')
    else:
        file = request.files['profile_pic']
        # store filename on db table
        cur = mysql.connection.cursor()
        cur.execute(f"insert into images (filename) values ('{app.config['UPLOAD_FOLDER'] + file.filename}');")
        cur.connection.commit()
        cur.close()
        
        # save file in the folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return render_template('upload_image.html', message='uploaded successfully')




# fetch
# cur = mysql.connection.cursor()
# cur.execute()
# one_user = cur.fetchone()
# cur.close()

# # create
# cur = mysql.connection.cursor()
# cur.execute()
# mysql.connection.commit()
# cur.close()


if __name__ == '__main__':
    app.run(debug=1)
