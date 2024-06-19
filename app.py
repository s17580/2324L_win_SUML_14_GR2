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

#Load data
df = pd.read_csv("data/results.csv")

uniq_teams_home = df['home_team'].unique()
uniq_teams_away = df['away_team'].unique()

# Konwersja wszystkich wartości na typ string
uniq_teams_home = [str(team) for team in uniq_teams_home]
uniq_teams_away = [str(team) for team in uniq_teams_away]

uniq_teams = np.union1d(uniq_teams_home, uniq_teams_away)

encoder= LabelEncoder()

def main():
    st.set_page_config(page_title="PJATK Football")
    st.header("PJATK Sports Bet")
    st.image("necessary_files/image/football_image.jpg")
    home_team = st.sidebar.selectbox("Wybierz Drużynę Gospodarzy", np.append("", uniq_teams))
away_team = st.sidebar.selectbox("Wybierz Drużynę Gości", np.append("", uniq_teams))
neutral = st.sidebar.selectbox("Czy Mecz odbywa się na Neutralnym Terenie?", [True, False])
tournament = st.sidebar.selectbox("Wybierz Turniej", np.append("", results['tournament'].unique()))
country = st.sidebar.selectbox("Wybierz Kraj", np.append("", results['country'].unique()))
city = st.sidebar.selectbox("Wybierz Miasto", np.append("", country_to_cities.get(country, [""])))