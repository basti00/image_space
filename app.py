from flask import Flask, render_template, request
import cv2
import plotly.graph_objects as go
import numpy as np
import seperate
import base64

app = Flask(__name__)

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
