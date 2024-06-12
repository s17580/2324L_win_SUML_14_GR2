# Prognozowanie Wyników Meczów Piłkarskich 

## Spis Treści 

- [Wprowadzenie](#wprowadzenie)
- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Uruchomienie Aplikacji](#uruchomienie-aplikacji)
- [Korzystanie z Aplikacji](#korzystanie-z-aplikacji)
- [Struktura Plików](#struktura-plików)
- [Kontakt](#kontakt)

## 1. Wprowadzenie 

Projekt ten ma na celu stworzenie aplikacji webowej do prognozowania wyników meczów piłkarskich. Aplikacja wykorzystuje modele uczenia maszynowego do przewidywania prawdopodobieństwa wygranej, remisu i przegranej na podstawie danych historycznych. Użytkownicy mogą wprowadzać dane dotyczące meczu i otrzymywać przewidywane wyniki wraz z wizualnymi efektami specjalnymi. 

## 2. Wymagania 

- Python 3.7+
- Streamlit
- Pandas
- Numpy
- Scikit-learn
- Pillow

## 3. Instalacja 

1. Sklonuj repozytorium:

    ```bash
    git clone https://github.com/s17580/2324L_win_SUML_14_GR2.git
    cd football-prediction
    ```

2. Utwórz i aktywuj wirtualne środowisko:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Dla Windows: .venv\Scripts\activate
    ```

3. Zainstaluj wymagane pakiety:

    ```bash
    pip install -r requirements.txt
    ```

## 4. Uruchomienie Aplikacji

Aby uruchomić aplikację, wykonaj następującą komendę w terminalu:

```bash
streamlit run footballPredRes.py

5. Korzystanie z Aplikacji

Po uruchomieniu aplikacji otworzy się strona webowa w przeglądarce.

W panelu bocznym wprowadź dane dotyczące meczu:

- Wybierz drużynę gospodarzy.
- Wybierz drużynę gości.
- Określ, czy mecz odbywa się na neutralnym terenie.
- Wybierz turniej.
- Wybierz miasto.
- Wybierz kraj.
- Wybierz datę meczu.
- Kliknij przycisk "Przewiduj", aby uzyskać przewidywane prawdopodobieństwo wygranej, remisu i przegranej.

Ostateczny wynik zostanie wyświetlony wraz z efektami specjalnymi.

Aby wyczyścić formularz, kliknij przycisk "Wyczyść formularz".

## 6. Struktura Plików

football-prediction/
├── footballPredRes.py
├── win_pred.pkl
├── draw_pred.pkl
├── results.csv
├── football_image.jpg
└── README.md

## 7. Kontakt

W razie jakichkolwiek pytań lub problemów, prosimy o kontakt na adres email: s17580@pjwstk.edu.pl
