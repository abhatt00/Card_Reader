from flask import Flask, render_template
from flask_pymongo import PyMongo
from scipy import ndimage, misc
import numpy as np
import os
import base64


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/BlackJack_cards"
mongo = PyMongo(app)


# converting an image to save it in mongo
with open("test.jpg", "rb") as imageFile:
    str = base64.b64encode(imageFile.read())
    # //store str in mongo
    print(str)

# to call each image back
with open("test2.jpg", "wb") as fimage:
    fimage.write(base64.b64decode(str))



path = "playing-cards-master/img/"
blackjack = mongo.db.BlackJack_cards.Card_Images


# iterate through the names of contents of the folder
for image_path in os.listdir(path):
    # create the full input path and read the file
    input_path = path + image_path

    with open(input_path, 'rb') as imageFile:
        my_string = base64.b64encode(imageFile.read())
        print(my_string)

    # with open(image_to_byte, "r") as imageFile:
    #     print(imageFile)
        # str = base64.b64encode(path + imageFile.read())
    #     # //store str in mongo
        blackjack.update_many({}, my_string, upsert=True)


# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# @app.route("/")
# def index():
#     # mars = mongo.db.mars.find_one()
#     return render_template("index.html", mars=mars)

# @app.route("/scrape")
# def scrape():
#     mars = mongo.db.mars
#     mars_data = scrape_mars.scrape_all()
#     mars.update({}, mars_data, upsert=True)
#     return "Scraping Successful!"

# MAKE SURE YOU UNCOMMENT ME vvv
if __name__ == "__main__":
    app.run()
