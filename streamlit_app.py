import os

import altair as alt
import pandas as pd
import streamlit as st
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import psycopg2
import psycopg2 as conn
from database import Base, SessionLocal, engine
from streamlit_extras.mention import mention

#load_dotenv()

#host = os.getenv("DB_HOST")
#user = os.getenv("DB_USER")
#password = os.getenv("DB_PASSWORD")
#dbname = os.getenv("DB_NAME")
#dbschema = os.getenv("DB_SCHEMA")
#dbtable = os.getenv("DB_TABLE")

#connexion SQL a partir du .env

#def get_conn():
#    return psycopg2.connect(
#        host=host,
#        database=dbname,
#        user=user,
#        password=password
#)


#import fichier CSS 

with open('./style.css') as f:
    css = f.read()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)

#Import CSV

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/Ligne_bon_vente.csv",
        sep=";",                  
        encoding="cp1252",
        encoding_errors="replace",
        on_bad_lines="skip",
        low_memory=False
    )


    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df

df = load_data()
    
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

#style
st.set_page_config(
    layout="wide"
)

#Personalisation tab NAV
st.set_page_config(
    page_title="Stat Coop",
    page_icon="asset/logo.png",
    layout="wide"
)

#Gestion thème 


if "mode_clair" not in st.session_state:
    st.session_state.mode_clair = False


def changer_theme():
    st.session_state.mode_clair = not st.session_state.mode_clair


st.button(
    "☀️/🌙",
    on_click=changer_theme
)


if st.session_state.mode_clair:

    st.markdown(
        """
        <style>

        /* PAGE CLAIRE */
        .stApp {
            background-color: #FFFFFF !important;
        }


        /* barre du haut Streamlit */
        header[data-testid="stHeader"] {
            background-color: #FFFFFF !important;
        }


        /* titre toujours vert */
        h1 {
            color: #228B22 !important;
        }


        /* textes */
        p, label, span {
            color: #000000 !important;
        }


        /* bouton */
        .stButton button {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 1px solid #228B22 !important;
        }


        /* tableau */
        div[data-testid="stDataFrame"] {
            background-color: #FFFFFF !important;
        }


        </style>
        """,
        unsafe_allow_html=True
    )


else:

    st.markdown(
        """
        <style>

        /* PAGE SOMBRE */
        .stApp {
            background-color: #0E1117 !important;
        }


        /* barre du haut Streamlit */
        header[data-testid="stHeader"] {
            background-color: #0E1117 !important;
        }


        /* titre toujours vert */
        h1 {
            color: #228B22 !important;
        }


        /* textes */
        p, label, span {
            color: #FAFAFA !important;
        }


        /* bouton */
        .stButton button {
            background-color: #0E1117 !important;
            color: #FAFAFA !important;
            border: 1px solid #228B22 !important;
        }


        /* tableau */
        div[data-testid="stDataFrame"] {
            background-color: #0E1117 !important;
        }


        </style>
        """,
        unsafe_allow_html=True
    )


#Titre page

st.title("StatCoop - Angélique MAIRE")

st.sidebar.image("asset/side_logo.png", width=270)
st.sidebar.markdown("Menu")

option = st.sidebar.selectbox(
    "Choisissez un tableau",
    ["Acceuil", "Par technicien", "Par engrais azotes"]
)

if option == "Acceuil":
    st.write("Choisir un tableau")
    
#////////////première page/////////////

elif option == "Par technicien":
    st.write("Statistiques par technicien")

    st.sidebar.markdown("Filtres")

    filtre = st.sidebar.selectbox(
        "Choisissez un filtre",
        ["Aucun","famille n°40","famille n°41","famille n°42","famille n°43","famille n°44","famille n°45","famille n°46"]
    )


# chagrement SQL
    
#    conn = get_conn()
#    cursor = conn.cursor()
#
#    cursor.execute(f"""
#        SELECT *
#        FROM {dbschema}.{dbtable}
#    """)
#
#    df = pd.DataFrame(
#        cursor.fetchall(),
#        columns=[desc[0] for desc in cursor.description]
#    )

#    cursor.close()


#CSV
    df = load_data()
    
    df.columns = df.columns.str.strip()


# filtres campagnes
    
    df = df[df["campagne_appro"].isin(["2024-2025", "2025-2026"])]

    df["quantite"] = pd.to_numeric(df["quantite"], errors="coerce")

    df_work = df.copy()


# sans filtre

    if filtre == "Aucun":

        df_table = pd.pivot_table(
            df_work,
            index=["technicien", "code_famille"],
            columns="campagne_appro",
            values="quantite",
            aggfunc="sum",
            fill_value=0
        )


# filtre
    else:

        code = filtre.replace("famille n°", "")

        df_work = df_work[
            df_work["code_famille"].astype(str) == code
        ]

        df_table = pd.pivot_table(
            df_work,
            index=["technicien", "famille_2"],
            columns="campagne_appro",
            values="quantite",
            aggfunc="sum",
            fill_value=0
        )


# evolution tech

    if "2024-2025" not in df_table.columns:
        df_table["2024-2025"] = 0
    if "2025-2026" not in df_table.columns:
        df_table["2025-2026"] = 0

    df_table["evolution_%"] = (
        (df_table["2025-2026"] - df_table["2024-2025"])
        / df_table["2024-2025"].replace(0, float("nan"))
    ) * 100


# Ajouter couleur

    def color_evolution(val):
        if pd.isna(val):
            return ""
        elif val > 0:
            return "color: green"
        elif val < 0:
            return "color: red"
        else:
            return ""


# AFFICHAGE

    df_table = df_table.reset_index()

    df_table["technicien"] = df_table["technicien"].mask(
        df_table["technicien"].duplicated()
    )

    st.dataframe(
        df_table.style
        .set_properties(**{
            "background-color": "#FFFFFF" if st.session_state.mode_clair else "#0E1117",
            "color": "#000000" if st.session_state.mode_clair else "#FAFAFA"
        })
    .format({
            "2024-2025": "{:.2f}",
            "2025-2026": "{:.2f}",
            "evolution_%": "{:.2f}%"
        })
        .map(
            color_evolution,
            subset=["evolution_%"]
        ),
        hide_index=True,
        use_container_width=True,
        height=600
    )
#    cursor.close()
#    conn.close()
    
    #Mention
    
    mention(
    label="Coopérative Interval 2026",
    icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgTwZ4hsOaMa8-6BhjmoiQBtPUnPuyynxXmg&s",
    url="https://www.interval.coop/",
    )  


#//////////////////////////////////////////////////////////////////////////////#

#Par engrais azotes deuxième page

elif option == "Par engrais azotes":
    st.write('Statistiques pas engrais azotes')


#    conn = get_conn()
#    cursor = conn.cursor()

#    cursor.execute(f"""
#        SELECT *
#        FROM {dbschema}.{dbtable}
#    """)

#    df = pd.DataFrame(
#        cursor.fetchall(),
#        columns=[desc[0] for desc in cursor.description]
#    )


#CSV

    df = load_data()
    
    df.columns = df.columns.str.strip()

# SQL

    df = df[df["campagne_appro"].isin(["2024-2025", "2025-2026"])]

    df["quantite"] = pd.to_numeric(df["quantite"], errors="coerce")

    df_work = df.copy()

    df_work = df_work[
        df_work["famille_2"] == "ENGRAIS AZOTES"
    ]

    df_work["pourcentage_azote"] = pd.to_numeric(
        df_work["pourcentage_azote"],
        errors="coerce"
    )

    df_work["unite_azote"] = (
        df_work["quantite"] *
        df_work["pourcentage_azote"] *
        1000
    )


# pivot

    df_table = pd.pivot_table(
        df_work,
        index=["technicien", "famille_2"],
        columns="campagne_appro",
        values=["quantite", "unite_azote"],
        aggfunc="sum",
        fill_value=0
    )

# fix bug affichage

    df_table.columns = [
        f"{col}_{campagne}"
        for col, campagne in df_table.columns
    ]


# mise en forme des évolutions et colones

    df_table["evolution_quantite_%"] = (
        (df_table["quantite_2025-2026"] - df_table["quantite_2024-2025"])
        / df_table["quantite_2024-2025"].replace(0, float("nan"))
    ) * 100

    df_table["evolution_unite_azote_%"] = (
        (df_table["unite_azote_2025-2026"] - df_table["unite_azote_2024-2025"])
        / df_table["unite_azote_2024-2025"].replace(0, float("nan"))
    ) * 100

    df_table = df_table.reset_index()

    df_table = df_table[
        [
            "technicien",
            "famille_2",

            "quantite_2024-2025",
            "quantite_2025-2026",
            "evolution_quantite_%",

            "unite_azote_2024-2025",
            "unite_azote_2025-2026",
            "evolution_unite_azote_%"
        ]
    ]


# ajout couleurs évolutions

    def color_evolution(val):
        if pd.isna(val):
            return ""
        elif val > 0:
            return "color: green"
        elif val < 0:
            return "color: red"
        return ""


# affichage tableau

    df_affichage = df_table.copy()

    df_affichage["technicien"] = df_affichage["technicien"].mask(
        df_affichage["technicien"].duplicated()
    )


    st.dataframe(
        df_affichage.style
        .set_properties(**{
            "background-color": "#FFFFFF" if st.session_state.mode_clair else "#0E1117",
            "color": "#000000" if st.session_state.mode_clair else "#FAFAFA"
        })
    .format({
            "quantite_2024-2025": "{:.2f}",
            "quantite_2025-2026": "{:.2f}",
            "unite_azote_2024-2025": "{:.2f}",
            "unite_azote_2025-2026": "{:.2f}",
            "evolution_quantite_%": "{:.2f}%",
            "evolution_unite_azote_%": "{:.2f}%"
        })
        .map(
            color_evolution,
            subset=[
                "evolution_quantite_%",
                "evolution_unite_azote_%"
            ]
        ),
        hide_index=True,
        use_container_width=True,
        height=600
    )

#Mention
    
    mention(
    label="Coopérative Interval 2026",
    icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgTwZ4hsOaMa8-6BhjmoiQBtPUnPuyynxXmg&s",
    url="https://www.interval.coop/",
    )    

# fermeture connexion

#    cursor.close()
#    conn.close()
    
