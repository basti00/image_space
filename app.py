from flask import Flask, render_template, request
import cv2
import plotly.graph_objects as go
import numpy as np
import seperate
import base64

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Configure logging
log_file = 'server.log'
max_bytes = 10e6
backup_count = 1

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    ]
)

app.logger.addHandler(logging.getLogger())

@app.before_request
def log_request_info():
    ip_address = request.remote_addr
    user_agent = request.user_agent.string
    app.logger.info('Request from IP: %s', ip_address)
    app.logger.info('User Agent: %s', user_agent)
    app.logger.info('Request: %s %s', request.method, request.url)
    #app.logger.info('Request headers: %s', request.headers)
    #app.logger.info('Request body: %s', request.get_data(as_text=True))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
        img_scaled = seperate.scale_down(img, 80)
        fig = seperate.seperate_plot(img_scaled)
    else:
        img = np.array([(0,0,0)])
        fig = seperate.seperate_plot(img)
        
    _, img_encoded = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')
    fig.update_layout(height=900, autosize=True)
    html = fig.to_html(full_html=False)
    #html = html.replace("450px", "100%")
    return render_template('index.html', plot=html, img_base64=img_base64)


if __name__ == '__main__':
    app.run(debug=False, port=5000)
