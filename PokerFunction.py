import pandas as pd

def poker(x):
    
    a = 0
    
    dd = pd.DataFrame({0: x[0], 1:x[1], 2: x[2], 3: x[3], 4:x[4], 5:x[5], 6:x[6], 7:x[7], 8:x[8], 9:x[9]},index=[0])
  
    from tensorflow.keras.models import load_model
    model = load_model("pokerhand.h5")

    prediction = model.predict_classes(dd)

    result = prediction
    
    if result == 4:
        a = a + 1
    
    if x[0] == x[2] == x[4] == x[6] == x[8]:
        result = 5
        if a == 1:
            result = 8

    if result == 0:
        result = "High Card"
    elif result == 1:
        result = "One pair"
    elif result == 2:
        result = "Two pairs"
    elif result == 3:
        result = "Three of a kind"
    elif result == 4:
        result = "Straight"
    elif result == 5:
        result = "Flush"
    elif result == 6:
        result = "Full house"
    elif result == 7:
        result = "Four of a kind"
    elif result == 8:
        result = "Straight flush"
    elif result == 9:
        result = "Royal flush"
  
    return result