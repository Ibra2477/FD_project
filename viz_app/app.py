import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="Photo Map", layout="wide")
st.title("Photo Map")

# ---------- Load data ----------
# Option A: CSV
# df = pd.read_csv("../data/points.csv")

# Option B: demo sample (replace this)
df = pd.DataFrame([
    {
        "id_photo": "p001",
        "id_photographe": "ph01",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "tags": "street,night",
        "description": "Night street scene near center.",
        "dates": "2025-04-12",
    },
    {
        "id_photo": "p002",
        "id_photographe": "ph02",
        "latitude": 48.8666,
        "longitude": 2.3322,
        "tags": "park,spring",
        "description": "Spring vibes in the park.",
        "dates": "2025-05-02",
    },
])

# ---------- Clean / normalize ----------
df["dates"] = pd.to_datetime(df["dates"], errors="coerce")

def normalize_tags(x):
    if isinstance(x, list):
        return [t.strip() for t in x if str(t).strip()]
    if pd.isna(x):
        return []
    return [t.strip() for t in str(x).split(",") if t.strip()]

df["tags_list"] = df["tags"].apply(normalize_tags)

# We display ALL points (no filters)
filtered = df.copy()

# ---------- Build map ----------
base = filtered if len(filtered) else df
center = [base["latitude"].mean(), base["longitude"].mean()]

m = folium.Map(location=center, zoom_start=12, tiles="OpenStreetMap")
cluster = MarkerCluster().add_to(m)

for _, row in filtered.iterrows():
    date_str = row["dates"].strftime("%Y-%m-%d") if pd.notna(row["dates"]) else ""
    tags_str = ", ".join(row["tags_list"])

    popup_html = f"""
    <div style="width: 260px;">
      <b>Photo:</b> {row.get('id_photo','')}<br>
      <b>Photographer:</b> {row.get('id_photographe','')}<br>
      <b>Date:</b> {date_str}<br>
      <b>Tags:</b> {tags_str}<br><br>
      <b>Description:</b><br>
      {row.get('description','')}
    </div>
    """

    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        tooltip=str(row.get("id_photo", "photo")),
        popup=folium.Popup(popup_html, max_width=300),
    ).add_to(cluster)

st_folium(m, width=None, height=650)

with st.expander("Show data"):
    st.dataframe(
        filtered[["id_photo", "id_photographe", "latitude", "longitude", "tags", "description", "dates"]],
        use_container_width=True
    )
