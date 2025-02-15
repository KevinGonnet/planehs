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

    # Filtrer : avions en vol, coordonnées valides
    df = df[df["on_ground"] == False].dropna(subset=["longitude", "latitude"])
    return df

def main():
    st.title("Dashboard Survol en Direct")

    if st.button("Afficher les stats et la carte"):
        df = fetch_flights()

        st.write(f"Nombre d'avions en vol détectés : {len(df)}")
        st.write(df.head())

        # Stats par pays d'origine (ordre décroissant)
        origin_counts = df["origin_country"].value_counts().sort_values(ascending=False)
        st.subheader("Répartition par pays d'origine (ordre décroissant)")
        st.bar_chart(origin_counts)

        # Afficher la carte des avions actuellement
        st.subheader("Carte des avions actuellement dans la zone")
        # Streamlit attend des colonnes 'lat' et 'lon'
        map_df = df.rename(columns={"latitude": "lat", "longitude": "lon"})
        st.map(map_df[["lat", "lon"]])

if __name__ == "__main__":
    main()
