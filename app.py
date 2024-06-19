import streamlit 
import pickle
import pandas as pd
import numpy as np
import streamlit as st

from datetime import datetime
from sklearn.preprocessing import LabelEncoder
#Initialize start time
startTime = datetime.now()

#Load the pre-trained model
#win_model = pickle.load(open('./ml_models/win_pred.pkl','rb'))

st.set_page_config(page_title="PJATK Football")
st.header("PJATK Sports Bet")
st.image("necessary_files/image/football_image.jpg")

#Load data
df = pd.read_csv("data/results.csv")

uniq_teams_home = df['home_team'].unique()
uniq_teams_away = df['away_team'].unique()

# Konwersja wszystkich wartości na typ string
uniq_teams_home = [str(team) for team in uniq_teams_home]
uniq_teams_away = [str(team) for team in uniq_teams_away]

uniq_teams = np.union1d(uniq_teams_home, uniq_teams_away)

encoder= LabelEncoder()
team_encoder = encoder.fit(uniq_teams)
tournament_encoder = encoder.fit(df["tournament"])
city_encoder = encoder.fit(df["city"])
country_endocer = encoder.fit(df["country"])

countrycity_walidation = df.groupby('country')['city'].unique().to_dict()

home_team = st.selectbox("Wybierz Drużynę Gospodarzy", np.append("", uniq_teams))
away_team = st.selectbox("Wybierz Drużynę Gości", np.append("", uniq_teams))
neutral = st.selectbox("Czy Mecz odbywa się na Neutralnym Terenie?", [True, False])
tournament = st.selectbox("Wybierz Turniej", np.append("", df['tournament'].unique()))
country = st.selectbox("Wybierz Kraj", np.append("", df['country'].unique()))
city = st.selectbox("Wybierz Miasto", np.append("", countrycity_walidation.get(country, [""])))

date = st.date_input("Wybierz Datę Meczu")