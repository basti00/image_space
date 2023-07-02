# Image Space

Plots an image in 3D space. Coordinates of each pixle are determined by the RGB value.

## Deploy on server

[Tutorial](https://www.twilio.com/blog/deploy-flask-python-app-aws)

Open the session running flask: 
```bash
tmux attach -t myApp
```
List all running sessions
```bash
tmux ls
```

In session start the flask server
```bash
cd ~/image_space/ && flask run --host=0.0.0.0 --port=8080
```

Press `ctrl+B` and then `D` to exit session

( `tmux new -s mytestapp` to create session )