import streamlit as st
import requests
import pandas as pd

def fetch_flights():
    # Définir la bounding box (ex. large autour de la France)
    url = "https://opensky-network.org/api/states/all"
    params = {
        "lamin": 41.0,
        "lomin": -5.0,
        "lamax": 51.0,
        "lomax": 10.0
    }

    response = requests.get(url, params=params)
    data = response.json()

    cols = [
        "icao24", "callsign", "origin_country", "time_position", "last_contact",
        "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
        "heading", "vertical_rate", "sensors", "geo_altitude", "squawk",
        "spi", "position_source"
    ]
    df = pd.DataFrame(data["states"], columns=cols)

    # Filtrer : avions en vol, coordos valides
    df = df[df["on_ground"] == False].dropna(subset=["longitude", "latitude"])
    return df

def main():
    st.title("Dashboard Survol en Direct")

    # Bouton pour déclencher l'affichage des stats
    if st.button("Afficher les stats des pays d'origine"):
        df = fetch_flights()
        st.write(f"Nombre d'avions en vol détectés : {len(df)}")

        # Afficher un aperçu du DataFrame
        st.write(df.head())

        # Stats par pays d'origine
        origin_counts = df["origin_country"].value_counts()
        st.subheader("Répartition par pays d'origine")
        st.bar_chart(origin_counts)

if __name__ == "__main__":
    main()
