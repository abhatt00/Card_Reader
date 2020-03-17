from time import time
import cv2
import numpy as np
import Cards
import os
# import VideoStream
import time
import PokerFunction


Five_Card_Hand = []

def CreateDeck(n_decks):
    # standard playing car deck, for blackjack (no suits)
    deck = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
            'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Spades', 'Diamonds',
            'Clubs', 'Hearts']

    # initialize card count, (always starts at zero)
    count = 0

    deck_state = {}
    for row in deck:
        deck_state[row] = 4 * n_decks

    return deck_state, count

# create a function to update the deck
def UpdateDeckState(DetectedCards, deck_state):
    for card in DetectedCards:
        deck_state[card.best_rank_match] = 0
        # need to consider how to update the deck but with limits,
        # e.g. only remove from deck if the card persists for a certain time
        #     or if a card of the same time appears right after in the same location, ignore
        return deck_state


# create a function to display the deck state
def DisplayDeckState(deck_state, image, font):
    H = 65
    cv2.putText(image, " Deck State ", (1100, 25), font, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(image, " -------- ", (1100, 40), font, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
    for k, v in deck_state.items():
        cv2.putText(image, k + ": " + str(v), (1100, H), font, 0.7, (0, 255, 0), 2,
                    cv2.LINE_AA)
        H += 20

    return image

def CountCards(deck_state, DetectedCards, count):
    # High cards (10, Jack, Queen, King and ace) count as -1
    # Low cards(2, 3, 4, 5 and 6) count as +1
    # the rest count as 0

    for card in DetectedCards:
        if card.best_rank_match in ('Ten', 'Jack', 'Queen', 'King', 'Ace'):
            count -= 1
            print("Detected a " + card.best_rank_match + " -1 to count")

        elif card.best_rank_match in ('Two', 'Three', 'Four', 'Five', 'Six'):
            count += 1
            print("Detected a " + card.best_rank_match + " +1 to count")

    deck_state = UpdateDeckState(DetectedCards, deck_state)

    print(count)

    return count, deck_state

n_decks = 1
deck_state, count = CreateDeck(n_decks)  # initialize the deck before main loop

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

        # set video size
        # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
        # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

        # self.window = cv2.namedWindow("test")

    def __del__(self):
        self.video.release()
        
    def get_frame2(self):
        ### ---- INITIALIZATION ---- ###
        # Define constants and initialize variables

        frame_rate_calc = 1
        freq = cv2.getTickFrequency()

        ## Define font to use
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Initialize camera object and video feed from the camera. The video stream is set up
        # as a seperate thread that constantly grabs frames from the camera feed.
        # See VideoStream.py for VideoStream class definition
        ## IF USING USB CAMERA INSTEAD OF PICAMERA,
        ## CHANGE THE THIRD ARGUMENT FROM 1 TO 2 IN THE FOLLOWING LINE:
        # videostream = VideoStream.VideoStream((IM_WIDTH,IM_HEIGHT),FRAME_RATE,1,0).start()
        # Give the camera time to warm up


        # Load the train rank and suit images
        path = os.path.dirname(os.path.abspath(__file__))
        train_ranks = Cards.load_ranks( path + '/Card_Imgs/')
        train_suits = Cards.load_suits( path + '/Card_Imgs/')

        # print(path + '/Card_Imgs/') # for debug

        ### ---- MAIN LOOP ---- ###
        # The main loop repeatedly grabs frames from the video stream
        # and processes them to find and identify playing cards.

        cam_quit = 0 # Loop control variable

        disp_deck_state = False # control if deck state is displayed

        # Begin capturing frames
        while cam_quit == 0:
                # Grab frame from video stream
                ret, image = self.video.read()

                # Start timer (for calculating frame rate)
                t1 = cv2.getTickCount()

                # Pre-process camera image (gray, blur, and threshold it)
                pre_proc = Cards.preprocess_image(image)
                
                # Find and sort the contours of all cards in the image (query cards)
                cnts_sort, cnt_is_card = Cards.find_cards(pre_proc)

                # If there are no contours, do nothing
                if len(cnts_sort) != 0:

                    # Initialize a new "cards" list to assign the card objects.
                    # k indexes the newly made array of cards.
                    cards = []
                    k = 0

                    # For each contour detected:
                    for i in range(len(cnts_sort)):
                        if (cnt_is_card[i] == 1):

                            # Create a card object from the contour and append it to the list of cards.
                            # preprocess_card function takes the card contour and contour and
                            # determines the cards properties (corner points, etc). It generates a
                            # flattened 200x300 image of the card, and isolates the card's
                            # suit and rank from the image.
                            cards.append(Cards.preprocess_card(cnts_sort[i],image))

                            # Find the best rank and suit match for the card.
                            cards[k].best_rank_match,cards[k].best_suit_match,cards[k].rank_diff,cards[k].suit_diff = Cards.match_card(cards[k],train_ranks,train_suits)

                            ## The card rank we need is here
                            ## We need 5 cards

                            # Draw center point and match result on the image.
                            image = Cards.draw_results(image, cards[k])
                            k = k + 1
                    
                    # Draw card contours on image (have to do contours all at once or
                    # they do not show up properly for some reason)
                    count = 0
                    if (len(cards) != 0):
                        temp_cnts = []

                        for i in range(len(cards)):
                            temp_cnts.append(cards[i].contour)
                            cv2.drawContours(image,temp_cnts, -1, (255,0,0), 2)

                        # BEGIN: MIKE BRYANT ADDED CODE
                        # -------------------------------------
                        # update deck state
                        UpdateDeckState(cards, deck_state)

                        # display number of cards detected
                        cv2.putText(image, "# of cards detected: " + str(len(cards)), (10, 50), font, 0.7, (0, 255, 0), 2,
                                        cv2.LINE_AA)

                        # display cards types detectedr
                        textY = 70  # text height, to be updated each loop
                        cv2.putText(image, " ", (10, textY), font, 0.7, (0, 255, 0), 2,
                                        cv2.LINE_AA)

                        textY += 25
                        cv2.putText(image, "count      card    ", (10, textY), font, 0.7, (0, 255, 0), 2,
                                    cv2.LINE_AA)

                        # add count a print to screen
                        # High cards (10, Jack, Queen, King and ace) count as -1
                        # Low cards(2, 3, 4, 5 and 6) count as +1
                        # the rest count as 0
                        i = 0
                        for card in cards:
                            textY += 25
                            i += 1

                            if card.best_rank_match in ('Ten', 'Jack', 'Queen', 'King', 'Ace'):
                                count -= 1
                                message = "  -1   " + str(card.best_rank_match) + " of " + str(card.best_suit_match)

                            elif card.best_rank_match in ('Two', 'Three', 'Four', 'Five', 'Six'):
                                count += 1
                                message = "  +1   " + str(card.best_rank_match) + " of " + str(card.best_suit_match)
                            else:
                                message = "   0   " + str(card.best_rank_match) + " of " + str(card.best_suit_match)

                            cv2.putText(image, message, (10, textY), font, 0.7, (0, 255, 0), 2,
                                                cv2.LINE_AA)
                            

                    if(len(cards) == 5):
                        Five_Card_Hand = []                 # Delete Previous Hand
                        for card in cards:

                            suit = card.best_suit_match     # Suit Match
                            rank = card.best_rank_match     # Number Match

                            # Convert Suit to match Ashkan's Code

                            if suit == "Hearts":
                                Five_Card_Hand.append("1")
                            elif suit == "Spades":
                                Five_Card_Hand.append("2")
                            elif suit == "Diamonds":
                                Five_Card_Hand.append("3")
                            elif suit == "Clubs":
                                Five_Card_Hand.append("4")

                            # Convert Rank to match Ashkan's Code
                            if rank == "Ace":
                                Five_Card_Hand.append("1")
                            elif rank == "Two":
                                Five_Card_Hand.append("2")
                            elif rank == "Three":
                                Five_Card_Hand.append("3")
                            elif rank == "Four":
                                Five_Card_Hand.append("4")
                            elif rank == "Five":
                                Five_Card_Hand.append("5")
                            elif rank == "Six":
                                Five_Card_Hand.append("6")
                            elif rank == "Seven":
                                Five_Card_Hand.append("7")
                            elif rank == "Eight":
                                Five_Card_Hand.append("8")
                            elif rank == "Nine":
                                Five_Card_Hand.append("9")
                            elif rank == "Ten":
                                Five_Card_Hand.append("10")
                            elif rank == "Jack":
                                Five_Card_Hand.append("11")
                            elif rank == "Queen":
                                Five_Card_Hand.append("12")
                            elif rank == "King":
                                Five_Card_Hand.append("13")
                        
                        print(Five_Card_Hand)

                        Hand = PokerFunction.poker(Five_Card_Hand)
                        print(Hand)
                            


                        message = "Current Count: " + str(count)
                        cv2.putText(image, message, (10, textY+25), font, 0.7, (0, 255, 0), 2,
                                    cv2.LINE_AA)
                        

                    # display deck state
                    if disp_deck_state:
                        DisplayDeckState(deck_state, image, font)

                    # -------------------------------------
                    # END: MIKE BRYANT ADDED CODE

                # Draw framerate in the corner of the image. Framerate is calculated at the end of the main loop,
                # so the first time this runs, framerate will be shown as 0.
                # cv2.putText(image, "FPS: "+ str(int(frame_rate_calc)),(10,26),font,0.7,(255,0,255),2,cv2.LINE_AA)

                if ret == True:
                    ret, jpeg = cv2.imencode('.jpg', image)
                    return jpeg.tobytes()

                # Finally, display the image with the identified cards!
                # Calculate framerate
                t2 = cv2.getTickCount()
                time1 = (t2-t1)/freq
                frame_rate_calc = 1/time1
                
                # Poll the keyboard. If 'q' is pressed, exit the main loop.
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    cam_quit = 1
                elif key == ord("r"):
                    if disp_deck_state:
                        disp_deck_state = False
                    else:
                        disp_deck_state = True


