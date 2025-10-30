import folium
import pandas as pd
from geopy.geocoders import Nominatim
from collections import Counter
import os

GEOCACHE = {}

def geocode_country(name):
    if name in GEOCACHE:
        return GEOCACHE[name]
    geo = Nominatim(user_agent="bibliometria_project")
    loc = geo.geocode(name, language='en', addressdetails=True)
    if loc:
        GEOCACHE[name] = (loc.latitude, loc.longitude)
        return GEOCACHE[name]
    return None

def build_heatmap(df, country_col='country', out_html='data/reports/map.html', out_png='data/reports/map.png'):
    # contar por país
    counts = Counter(df[country_col].dropna().astype(str).str.strip().tolist())
    m = folium.Map(location=[20,0], zoom_start=2)
    for c, cnt in counts.items():
        coords = geocode_country(c)
        if coords:
            folium.CircleMarker(location=coords, radius=3+cnt/2, popup=f"{c}: {cnt}").add_to(m)
    m.save(out_html)
    # Para PNG: usar selenium or save screenshot; else instruct user to open HTML
    return out_html
