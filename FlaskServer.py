import os
from flask import Flask, request, render_template
from werkzeug import secure_filename
import datetime

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['jpg'])


class MyServer(Flask):
    def __init__(self, *args, **kwargs):
        super(MyServer, self).__init__(*args, **kwargs)
        # Weather Data
        self.last_updated = "---"
        self.wind_spead = '-'
        self.wind_direction = '-'
        self.outside_temp = '-'
        self.inside_temp = '-'
        self.humidity = '-'
        self.pressure = '-'


app = MyServer(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_time_string():
    return datetime.datetime.now().strftime("%-H:%M - %m/%d/%Y")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['weather.jpg']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            app.last_updated = get_time_string()
            return "yay!"
    return ":("


@app.route('/weatherdata', methods=['POST'])
def upload_weather():
    last_updated = get_time_string()
    return "done"


@app.route('/', methods=['GET'])
def return_main():
    return render_template("main.html",
                           last_update=app.last_updated,
                           wind_spead=app.wind_spead,
                           wind_direction=app.wind_direction,
                           out_temp=app.outside_temp,
                           in_temp=app.inside_temp,
                           humidity=app.humidity,
                           pressure=app.pressure)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
