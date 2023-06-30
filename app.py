from flask import Flask, render_template, request
import cv2
import plotly.graph_objects as go
import numpy as np
import seperate

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the uploaded file from the request
        file = request.files['file']
        # Read and analyze the image using OpenCV (you can replace this with your own analysis code)
        img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
        # Perform your analysis on 'img' here

        # Generate Plotly graph based on analysis results
        #fig = go.Figure(data=go.Scatter(x=[1, 2, 3], y=[6, 5, 6]))

        image = seperate.scale_down(img, 80)
        fig = seperate.seperate_plot(image)
        fig.update_layout(height=1000, autosize=True)
        return render_template('index.html', plot=fig.to_html(full_html=False))

    fig = go.Figure(data=go.Scatter(x=[1, 2, 3], y=[4, 5, 6]))

    fig = seperate.seperate_plot(np.array([]))
    fig.update_layout(height=1000, autosize=True)
    #return render_template('result.html', plot=fig.to_html(full_html=False))
    
    return render_template('index.html', plot=fig.to_html(full_html=False))


if __name__ == '__main__':
    app.run(debug=True)