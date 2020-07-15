# IMAGE RECOGNITION THROUGH MACHINE LEARNING

## Run app.py and go to 127.0.0.1:5000 to start card detection

Card detection based on the number and suit displayed on the corner of each playing card.
Using Python to access the laptop webcam, take each frame as a singular image and recognize the five cards in the webcam window.
Once five cards are recognized by the camera, the image is analyzed for each card number and each suit.
The best available five-card Poker hand is displayed in the terminal window.

Webpage:
[Main screen](Webcam_cards_img.png)

MongoDB:
[Main screen](MongoDB_webpage.png)

We utilized MongoDB to take each recognized image and convert it to a string, then convert it back to an image once the correct card value is shown.
