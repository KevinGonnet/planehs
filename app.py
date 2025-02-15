import streamlit as st
import requests
import pandas as pd

def fetch_flights_haute_savoie():
    # Bounding box "Haute-Savoie" (approx)
    url = "https://opensky-network.org/api/states/all"
    params = {
        "lamin": 45.73,  # latitude min
        "lomin": 5.6,    # longitude min
        "lamax": 46.46,  # latitude max
        "lomax": 7.2     # longitude max
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

    # Filtrer : avions en vol + coordonnées valides
    df = df[df["on_ground"] == False].dropna(subset=["longitude", "latitude"])
    return df

def main():
    st.title("Dashboard Survol - Haute-Savoie")

    if st.button("Afficher les stats et la carte"):
        df = fetch_flights_haute_savoie()

        st.write(f"Nombre d'avions détectés en vol : {len(df)}")
        st.write(df.head())

        # Stats par pays d'origine (ordre décroissant)
        origin_counts = df["origin_country"].value_counts().sort_values(ascending=False)
        st.subheader("Répartition par pays d'origine (ordre décroissant)")
        st.bar_chart(origin_counts)

        # Afficher la carte des avions actuellement dans la zone
        st.subheader("Carte des avions au-dessus de la Haute-Savoie")
        # Streamlit attend des colonnes 'lat' et 'lon'
        map_df = df.rename(columns={"latitude": "lat", "longitude": "lon"})
        st.map(map_df[["lat", "lon"]])

if __name__ == "__main__":
    main()
