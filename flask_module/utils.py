from opencv_module import utils
from flask import Flask, render_template, Response
app = Flask(__name__)

@app.route('/video-feed')
def video_feed():
    return Response(utils.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

def flask_start():
    print(f'Starting...')
    app.run(debug=True)