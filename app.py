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
win_model = pickle.load(open('./ml_models/win_pred.pkl','rb'))

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

def predict_result(home_team, away_team, neutral, tournament, city, country, date):
    if home_team == away_team:
        # Jeśli wybrane drużyny są takie same, zwróć remis
        return 0, 1, 0

    # Kodowanie wartości
    home_team_encoded = team_encoder.transform([home_team])[0]
    away_team_encoded = team_encoder.transform([away_team])[0]
    tournament_encoded = tournament_encoder.transform([tournament])[0]
    city_encoded = city_encoder.transform([city])[0]
    country_encoded = countrycity_walidation.transform([country])[0]
    
    # Zakodowanie daty jako string
    date_encoded = LabelEncoder().fit_transform([str(date)])[0]

    # Utworzenie DataFrame z danymi wejściowymi
    input_data = pd.DataFrame({
        'date': [date_encoded],
        'home_team': [home_team_encoded],
        'away_team': [away_team_encoded],
        'home_score': [1],  # Możesz dostosować zgodnie z wymaganiami modelu
        'tournament': [tournament_encoded],
        'city': [city_encoded],
        'country': [country_encoded],
        'neutral': [neutral]
    })

    # Ustawienie odpowiedniej kolejności kolumn
    expected_columns = ['date', 'home_team', 'away_team', 'home_score', 'tournament', 'city', 'country', 'neutral']
    input_data = input_data[expected_columns]

    # Wyświetlenie danych wejściowych dla celów diagnostycznych
    st.write("Dane wejściowe do predykcji:", input_data)

    # Przewidywanie wyników
    win_prob = win_model.predict_proba(input_data)[0][1]
    

    return win_prob

predict = predict_result(home_team, away_team, neutral, tournament, city, country, date)