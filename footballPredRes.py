import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from PIL import Image
import streamlit.components.v1 as components

# Wczytywanie zapisanych modeli
st.write("Uruchamiam aplikację...")

try:
    with open("win_pred.pkl", "rb") as file:
        win_model = pickle.load(file)
        st.write("Załadowano model win_pred.pkl")
except Exception as e:
    st.write(f"Błąd podczas wczytywania modelu win_pred.pkl: {e}")

try:
    with open("draw_pred.pkl", "rb") as file:
        draw_model = pickle.load(file)
        st.write("Załadowano model draw_pred.pkl")
except Exception as e:
    st.write(f"Błąd podczas wczytywania modelu draw_pred.pkl: {e}")

# Wczytywanie danych
try:
    results = pd.read_csv("results.csv")
    st.write("Wczytano plik results.csv")
except Exception as e:
    st.write(f"Błąd podczas wczytywania pliku results.csv: {e}")

# Pobranie unikalnych wartości drużyn
uniq_teams_home = results['home_team'].unique()
uniq_teams_away = results['away_team'].unique()

# Konwersja wszystkich wartości na typ string
uniq_teams_home = [str(team) for team in uniq_teams_home]
uniq_teams_away = [str(team) for team in uniq_teams_away]

# Unia zestawów drużyn
uniq_teams = np.union1d(uniq_teams_home, uniq_teams_away)

# LabelEncoder do kodowania drużyn i innych cech
team_encoder = LabelEncoder()
team_encoder.fit(uniq_teams)

tournament_encoder = LabelEncoder()
tournament_encoder.fit(results['tournament'])

city_encoder = LabelEncoder()
city_encoder.fit(results['city'])

country_encoder = LabelEncoder()
country_encoder.fit(results['country'])

# Mapa krajów do miast
country_to_cities = results.groupby('country')['city'].unique().to_dict()

# Funkcja do przewidywania wyniku
def predict_result(home_team, away_team, neutral, tournament, city, country, date):
    if home_team == away_team:
        # Jeśli wybrane drużyny są takie same, zwróć remis
        return 0, 1, 0

    # Kodowanie wartości
    home_team_encoded = team_encoder.transform([home_team])[0]
    away_team_encoded = team_encoder.transform([away_team])[0]
    tournament_encoded = tournament_encoder.transform([tournament])[0]
    city_encoded = city_encoder.transform([city])[0]
    country_encoded = country_encoder.transform([country])[0]
    
    # Zakodowanie daty jako string
    date_encoded = LabelEncoder().fit_transform([str(date)])[0]

    # Utworzenie DataFrame z danymi wejściowymi
    input_data = pd.DataFrame({
        'date': [date_encoded],
        'home_team': [home_team_encoded],
        'away_team': [away_team_encoded],
        'home_score': [0],  # Możesz dostosować zgodnie z wymaganiami modelu
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
    draw_prob = draw_model.predict_proba(input_data)[0][1]
    loss_prob = 1 - win_prob - draw_prob

    return win_prob, draw_prob, loss_prob

# Tworzenie interfejsu użytkownika w Streamlit
st.title("Prognozowanie Wyniku Meczów Piłkarskich")

# Dodanie obrazu do aplikacji
image = Image.open("football_image.jpg")
st.image(image, caption='Prognozowanie wyników meczów piłkarskich', use_column_width=True)

st.sidebar.header("Parametry Wejściowe")

home_team = st.sidebar.selectbox("Wybierz Drużynę Gospodarzy", np.append("", uniq_teams))
away_team = st.sidebar.selectbox("Wybierz Drużynę Gości", np.append("", uniq_teams))
neutral = st.sidebar.selectbox("Czy Mecz odbywa się na Neutralnym Terenie?", [True, False])
tournament = st.sidebar.selectbox("Wybierz Turniej", np.append("", results['tournament'].unique()))
city = st.sidebar.selectbox("Wybierz Miasto", np.append("", results['city'].unique()))
country = st.sidebar.selectbox("Wybierz Kraj", np.append("", results['country'].unique()))
date = st.sidebar.date_input("Wybierz Datę Meczu")

# Aktualizacja listy miast po zmianie kraju
if country:
    st.sidebar.selectbox("Wybierz Miasto", np.append("", country_to_cities.get(country, [""])))

# Walidacja formularza
if st.sidebar.button("Przewiduj"):
    if not home_team:
        st.sidebar.error("Wybierz Drużynę Gospodarzy!")
    elif not away_team:
        st.sidebar.error("Wybierz Drużynę Gości!")
    elif not tournament:
        st.sidebar.error("Wybierz Turniej!")
    elif not city:
        st.sidebar.error("Wybierz Miasto!")
    elif not country:
        st.sidebar.error("Wybierz Kraj!")
    elif city not in country_to_cities.get(country, []):
        st.sidebar.error(f"Wybrane miasto {city} nie znajduje się w kraju {country}!")
    else:
        st.write(f"Drużyna Gospodarzy: {home_team}")
        st.write(f"Drużyna Gości: {away_team}")
        st.write(f"Neutralne Miejsce: {neutral}")
        st.write(f"Turniej: {tournament}")
        st.write(f"Miasto: {city}")
        st.write(f"Kraj: {country}")
        st.write(f"Data: {date}")

        win_prob, draw_prob, loss_prob = predict_result(home_team, away_team, neutral, tournament, city, country, date)

        # Wyświetlenie wyników predykcji
        st.write(f"Prawdopodobieństwo Wygranej dla {home_team}: {win_prob*100:.2f}%")
        st.write(f"Prawdopodobieństwo Remisu: {draw_prob*100:.2f}%")
        st.write(f"Prawdopodobieństwo Przegranej dla {away_team}: {loss_prob*100:.2f}%")

        # Wyświetlenie ostatecznego wyniku
        if win_prob > draw_prob and win_prob > loss_prob:
            final_result = f"Ostateczny wynik: Wygrana dla {home_team}"
        elif draw_prob > win_prob and draw_prob > loss_prob:
            final_result = "Ostateczny wynik: Remis"
        else:
            final_result = f"Ostateczny wynik: Wygrana dla {away_team}"
        
        st.write(final_result)

        # Dodanie efektów specjalnych po wykonaniu przewidywania
        st.balloons()
        st.success(final_result)

        # Czyszczenie formularza
        if st.sidebar.button("Wyczyść formularz"):
            st.experimental_rerun()