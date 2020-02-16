from flask import Flask, render_template, Response
#from flask_pymongo import PyMongo
from scipy import ndimage, misc
import numpy as np
import os
import base64
from camera import VideoCamera



app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# app = Flask(__name__)

# # Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/BlackJack_cards"
# mongo = PyMongo(app)


# # converting an image to save it in mongo
# with open("test.jpg", "rb") as imageFile:
#     str = base64.b64encode(imageFile.read())
#     # //store str in mongo
#     print(str)

# # to call each image back
# with open("test2.jpg", "wb") as fimage:
#     fimage.write(base64.b64decode(str))



# path = "playing-cards-master/img/"
# blackjack = mongo.db.BlackJack_cards.Card_Images


# # iterate through the names of contents of the folder
# for image_path in os.listdir(path):
#     # create the full input path and read the file
#     input_path = path + image_path

#     with open(input_path, 'rb') as imageFile:
#         my_string = base64.b64encode(imageFile.read())
#         print(my_string)

#     # with open(image_to_byte, "r") as imageFile:
#     #     print(imageFile)
#         # str = base64.b64encode(path + imageFile.read())
#     #     # //store str in mongo
#         blackjack.update_one({}, my_string, upsert=True)


if __name__ == "__main__":
    app.run()
