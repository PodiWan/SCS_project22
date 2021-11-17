import asyncio
from opencv_module import utils
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__)
async_mode = None
socket_ = SocketIO(app, async_mode=async_mode)

@app.route('/video-feed')
def video_feed():
    return Response(utils.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_.async_mode)

def flask_start():
    print(f'Starting...')
    socket_.run(app=app, host='0.0.0.0', port=5000)