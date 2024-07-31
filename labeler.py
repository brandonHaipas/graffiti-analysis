import pandas as pd
import re
from PIL import Image

data = pd.read_csv("links_and_file_names.csv")
columns = data.columns.tolist()

if "label" not in columns:
    data["label"] = ""
    
emotion_list = ["sadness", "joy", "trust", "fear", "surprise", "disgust", "anger", "anticipation"]
pattern = re.compile(r'^(' + '|'.join(emotion_list) + r')(-(' + '|'.join(emotion_list) + '))*$')
previous_col = data['label'].tolist()

i = 0
new_col = []
for index, row in data.iterrows():
    if row.iloc[2] != "":
        new_col.append(row[2])
        pass
    else:
        ready = False
        while not ready:
            image = Image.open(f"./images/{row.iloc[1]}")
            image.show()
            print("Write the emotions that this image transmit to you separated by hyphens, the emotions that you can choose are: \n")
            for em in emotion_list:
                print(f"- {em}")
            emotions = input("Your input: \n")
            if pattern.match(emotions):
                # save the emotions
                new_col.append(emotions)
                ready = True
            else:
                # ask again
                print("The input isn't valid!\n")
                pass
    i+=1
    if i < len(previous_col):
        choice = input("Do you wish to continue labeling? (Y/n)")
        if choice == 'Y' or choice =='y':
            pass
        if choice == 'N' or choice == 'n':
            # fill the rest of the column with the rest of the values
            new_col += previous_col[i:]
            break

data["label"] = new_col
data.to_csv('dataset.csv')