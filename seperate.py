import plotly.express as px
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
import plotly.graph_objects as go
import pandas as pd

def rgb_to_hex(red, green, blue):
    '''Return color as #rrggbb for the given color values.'''
    return f'rgb({",".join([str(c) for c in [blue, green, red]])})'

def load_image(image_path):
    if image_path is None:
        return
    name = image_path.split('.')[0]

    # Load the image using OpenCV
    image = cv2.imread(image_path)
    
    return image, name

def scale_down(image, width, just_fig=False):
    # Get the original dimensions of the image
    original_width, original_height = image.shape[:2]

    # Calculate the aspect ratio of the original image
    aspect_ratio = original_width / original_height

    # Calculate the desired height of the resized image
    # by dividing the desired width by the aspect ratio
    desired_height = width / aspect_ratio

    # Use cv2.resize() to downsample the image to the desired dimensions
    resized_image = cv2.resize(image, (width, int(desired_height)))

    return resized_image

def seperate_plot(image, name='', save_html=False):
    # Convert the image to a 3D numpy array, where the dimensions
    # represent the red, green, and blue channels of the image
    print(image.shape)
    samples = image.reshape(-1, 3)

    print(samples.shape)
    # Create a plotly figure using the scatter3d function, which
    # will plot the 3D samples as a scatter plot
    
    df = pd.DataFrame(samples)
    df.loc[len(df.index)] = [0,0,0]
    df.loc[len(df.index)] = [255,0,0]
    df.loc[len(df.index)] = [0,255,0]
    df.loc[len(df.index)] = [0,0,255]
    df.loc[len(df.index)] = [0,255,255]
    df.loc[len(df.index)] = [255,0,255]
    df.loc[len(df.index)] = [255,255,0]
    df.loc[len(df.index)] = [255,255,255]

    df = df.drop_duplicates()

    print(df.shape)

    df['hex'] = df.apply(lambda r: rgb_to_hex(*r), axis=1)
    
    fig = go.Figure(data=[go.Scatter3d(
        x=df[0], y=df[1], z=df[2],
        mode='markers',
        marker_color=df['hex'],
    )])
    fig.update_traces(marker_size = 2)

    # tight layout
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.update_layout(template='plotly_dark')
    if save_html:
        fig.write_html(f'{name}_3D_plot_new.html')
    
    
    return fig


def do(image_path):
    image, _ = load_image(image_path)
    image = scale_down(image)
    fig = seperate_plot(image, save_html=False)
    fig.show()

if __name__ == '__main__':
    # x and y given as array_like objects

    abso = 'C:/Users/uhlse/OneDrive/Desktop/Stuff/Projects/pixels in 3D space/'
    do(abso+'img/img2.jpg')

    '''
    do(abso+'img/img.png')
    do(abso+'img/car.webp')
    do(abso+'img/allcolors.png')
    do(abso+'img/flower.webp')
    do(abso+'img/img3.jfif')
    do(abso+'img/colorwheel.webp')
    ''' 