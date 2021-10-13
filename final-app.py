import streamlit as st
import cv2
import pandas as pd
import warnings

warnings.filterwarnings("ignore")
data3 = pd.read_csv("data3.csv", encoding='latin-1')

recommended_songs = data3.iloc[0:5]

def reset_index(table):
    table.reset_index()
    table.drop(columns = 'Unnamed: 0', inplace = True, axis = 1)

# Get the data

happy_imp = data3[((data3["nrgy"] > 80) & (data3["dnce"] > 60) & (data3["val"] > 40))]
reset_index(happy_imp)

sad_imp = data3[((data3["nrgy"] < 50) &  (data3["dnce"] < 50) & (data3["val"] < 35))]
reset_index(sad_imp)

tense_imp = data3[((data3["nrgy"] > 60) &  (data3["dnce"] < 50) & (data3["val"] < 30))]
reset_index(tense_imp)

excited_imp = data3[((data3["nrgy"] > 70) &  (data3["dnce"] > 65) & (data3["val"] > 70))]
reset_index(excited_imp)

neutral_imp = data3[((data3["nrgy"] > 60) & (data3["nrgy"] < 70) & (data3["bpm"] > 100) & (data3["bpm"] < 140) & (data3["dnce"] > 55) & (data3["dnce"] < 70) & (data3["val"] > 40) & (data3["val"] < 65))]
reset_index(neutral_imp)

# Get the emotion
emotions = {"Joy": happy_imp, "Sadness": sad_imp, "Anger": tense_imp, "Neutral": neutral_imp}
emotion_detected = "Anger"

def EmotionSongGenerator(emotions, emotion_detected):
    for emotion in emotions.keys():
        if emotion_detected == emotion:
            global recommended_songs
            recommended_songs = emotions[emotion].sample(5)
    return recommended_songs


def getSongs():
    data_shown = sad_imp.sample(5)
    global recommended_songs
    recommended_songs = data_shown
    return recommended_songs

st.title("Music Recommendation using Emotion")
st.write("Option 1 - Enter a passage of text")

st.text_area("Enter text for NLP")
st.button("Generate Recommendations", key = "first", on_click=getSongs)

st.write("For the time being, here's 5 random songs until you input something.😁")
placeholder = st.empty()
songs_to_display = EmotionSongGenerator(emotions, emotion_detected)
placeholder.write(songs_to_display[["title", "artist", "top genre", "year"]])

# print(songs_to_display[songs_to_display["title"] == "Hey, Soul Sister"])

st.write("Option 2 - Use your web cam")
run = st.checkbox('Run')

FRAME_WINDOW = st.image([])
camera = cv2.VideoCapture(0)

while run:
    _, frame = camera.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    FRAME_WINDOW.image(frame)
else:
    st.write('Camera is off')

st.button("Generate Recommendations", key = "second")



