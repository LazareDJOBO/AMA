import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import unicodedata
from score_composite import calcul_scoreComposite

# ============================
# CONFIGURATION DE LA PAGE
# ============================
st.set_page_config(
    page_title="Dashbord général",
    page_icon="🩺",
    layout="wide"
)

# ============================
# STYLE CSS PROFESSIONNEL
# ============================
st.markdown("""
<style>

.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 1.5rem !important;
    padding-left: 3.5rem !important;
    padding-right: 3.5rem !important;
    background-color: #F8FAFC;
}

/* Titres */
h1 {
    text-align: center;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 2rem;
}

h2, h3 {
    color: #1E293B;
}

/* KPI Cards */
.kpi-card {
    background: white;
    border-radius: 12px;
    padding: 1.3rem;
    text-align: center;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
}

.kpi-title {
    font-size: 14px;
    color: #64748B;
}

.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #0F172A;
}

/* Légende */
.legend-box {
    background: white;
    padding: 1.3rem;
    border-radius: 12px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ============================
# IMPORTATION DES DONNÉES
# ============================
@st.cache_data


def load_data(file):
    fl = pd.read_csv("Data AI4CKD - Original.csv")
    df = fl.drop(index=[306,307,308], errors='ignore')

    df = fl[["Adresse (Département)"]]
    for col in ["Sexe_M", "Age","DFG_calcule","niveau_risque","score_composite","DFG_calcule"]:
        df[col] = file[col]

    df = df.dropna(subset=["Adresse (Département)"])
    # 

    # df = df.apply(lambda col: col.str.replace(',', '.', regex=False)
    #               if col.dtype == 'object' else col)

    # df = df.apply(pd.to_numeric, errors='ignore')
    # df = df.dropna(subset=['Créatinine (mg/L)', 'Age', 'Sexe', 'Adresse (Département)'])
    # df = df[df['Créatinine (mg/L)'] > 0]

    return df

file = pd.read_csv("Data AI4CKD - Original.csv")

#========================
# calcule du score composite
#========================
df_scores = calcul_scoreComposite(file)

df = load_data(df_scores)


# ============================
# FILTRES INTERACTIFS
# ============================
st.markdown("<p style='color:black;font-size:30px;padding-top:2rem'>🩺 Dashboard Score Composite – Maladie Rénale Chronique</p>", 
            unsafe_allow_html=True)

col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    sexe_selection = st.selectbox("Sexe", ["Tous", "M", "F"] )
    if sexe_selection != "Tous":
        if sexe_selection == "M":
            sexe_selection = 1
        elif sexe_selection == "F":
            sexe_selection = 0
        df = df[df["Sexe_M"] == sexe_selection]

with col_filter2:
    age_range = st.slider("Tranche d'âge", int(df["Age"].min()), int(df["Age"].max()), (int(df["Age"].min()), int(df["Age"].max())))
    df = df[(df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1])]

st.divider()


# ============================
# KPI CARDS
# ============================
# KPI Cards par niveau de risque ---

palette = {"Faible":"#22C55E","Moyen":"#F59E0B","Élevé":"#DC2626"}
col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)

with col_kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Patients analysés</div>
        <div class="kpi-value">{len(df)}</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Score moyen composite</div>
        <div class="kpi-value">{df['score_composite'].mean():.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# KPI pour chaque niveau
with col_kpi3:
    count_faible = (df["niveau_risque"]=="Faible").sum()
    st.markdown(f"""
    <div class="kpi-card" style="border-left:6px solid {palette['Faible']};">
        <div class="kpi-title">Patients niveau Faible</div>
        <div class="kpi-value">{count_faible}</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    count_moyen = (df["niveau_risque"]=="Modéré").sum()
    st.markdown(f"""
    <div class="kpi-card" style="border-left:6px solid {palette['Moyen']};">
        <div class="kpi-title">Patients niveau Moyen</div>
        <div class="kpi-value">{count_moyen}</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi5:
    count_eleve = (df["niveau_risque"]=="Élevé").sum()
    st.markdown(f"""
    <div class="kpi-card" style="border-left:6px solid {palette['Élevé']};">
        <div class="kpi-title">Patients niveau Élevé</div>
        <div class="kpi-value">{count_eleve}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()


df_prevalence = df.groupby("Adresse (Département)")["score_composite"].mean().reset_index()
df_prevalence["proportion"] = df_prevalence["score_composite"]
# ============================
# NETTOYAGE DES NOMS
# ============================
def nettoyer_nom(texte):
    nfkd = unicodedata.normalize('NFKD', str(texte))
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).upper().strip()

df_prevalence["Adresse (Département)"] = df_prevalence["Adresse (Département)"].apply(nettoyer_nom)

# ============================
# TITRE
# ============================


# ============================
# CARTE INTERACTIVE
# ============================

df_tooltip = df.groupby("Adresse (Département)").agg(
    score_moyen=("score_composite", "mean"),
    nb_patients=("score_composite", "count"),
    pct_eleve=("niveau_risque", lambda x: (x=="Élevé").mean()*100)
).reset_index()

df_tooltip["score_moyen"] = df_tooltip["score_moyen"].round(2)
df_tooltip["pct_eleve"] = df_tooltip["pct_eleve"].round(1)

with open("geoBoundaries-BEN-ADM1.geojson", encoding="utf-8") as f:
    geojson_data = json.load(f)

stats_dict = df_tooltip.set_index("Adresse (Département)").to_dict("index")


CLE_GEO = "shapeName"
for feature in geojson_data["features"]:
    dep = feature["properties"][CLE_GEO]
    if dep in stats_dict:
        feature["properties"].update(stats_dict[dep])
    else:
        feature["properties"].update({
            "score_moyen": 0,
            "nb_patients": 0,
            "pct_eleve": 0
        })


for feature in geojson_data["features"]:
    feature["properties"][CLE_GEO] = nettoyer_nom(feature["properties"][CLE_GEO])

m = folium.Map(location=[9.5, 2.5], zoom_start=7, tiles="CartoDB positron")

folium.Choropleth(
    geo_data=geojson_data,
    data=df_prevalence,
    columns=["Adresse (Département)", "proportion"],
    key_on=f"feature.properties.{CLE_GEO}",
    fill_color="YlOrRd",
    bins=[0, 30, 60, 100],
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="black",
    nan_fill_opacity=0.3,
    
).add_to(m)

col_map, col_leg = st.columns([3,1])

with col_map:
    st_folium(m, use_container_width=True, height=520)
    st.markdown("<p style='color:black;font-size:18px;'>Carte interactive des zones à risque rénal au Bénin</p>", 
            unsafe_allow_html=True)


with col_leg:
    st.markdown("<div class='legend-box'>", unsafe_allow_html=True)
    st.markdown("<p style='color:gray;font-size:18px'>Légende</p>", 
            unsafe_allow_html=True)
    st.markdown("<p style='color:gray;font-size:14px'>Classification basée sur le DFG (CKD-EPI 2021).</p>", 
            unsafe_allow_html=True)


    def leg(c, t, d):
        st.markdown(f"""
        <div style="display:flex;align-items:center;margin-bottom:10px;">
            <div style="width:22px;height:22px;background:{c};border-radius:4px;margin-right:10px;"></div>
            <div style="color:black"><b>{t}</b><br>
            <small style="color: gray;">{d}</small></div>

        </div>
        """, unsafe_allow_html=True)

    leg("#DC2626", "+60% : Zone critique.","Priorité absolue pour le dépistage, la prévention et la prise en charge spécialisée.")
    leg("#F59E0B", "30–60% : Zone à risque élevé", "Renforcement du dépistage précoce, suivi médical et sensibilisation communautaire.")
    leg("#FDE68A", "0–30% : Zone sous surveillance","Surveillance régulière et actions de prévention primaire.")

    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ============================
# GRAPHIQUE
# ============================
st.subheader("📊 Prévalence par département")
df_plot = df_prevalence.sort_values("proportion", ascending=False)
st.bar_chart(df_plot.set_index("Adresse (Département)")["proportion"], sort="proportion")

#
# --- 6️⃣ Tableau interactif des patients filtrés ---
st.subheader("🗂 Détails des patients filtrés")
import numpy as np

df["Sexe"] = np.where(df["Sexe_M"] == 1, "M", "F")

colonnes_affichees = [
    "Adresse (Département)",
    "Age",
    "Sexe",
    "niveau_risque",
    "score_composite"
]

st.dataframe(
    df[colonnes_affichees].sort_values("score_composite", ascending=False),
    use_container_width=True)

st.caption("Source : Données cliniques AI4CKD – Traitement & visualisation Python + Streamlit")