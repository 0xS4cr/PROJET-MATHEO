import os

import altair as alt
import pandas as pd
import streamlit as st
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import psycopg2
from database import Base, SessionLocal, engine


load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dbname = os.getenv("DB_NAME")
dbschema = os.getenv("DB_SCHEMA")
dbtable = os.getenv("DB_TABLE")

#connexion SQL a partir du .env

conn = psycopg2.connect(
    host=host,
    database=dbname,
    user=user,
    password=password
)


#import fichier CSS 

with open('./style.css') as f:
    css = f.read()
    #st.write("CSS chargé")
    
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


#Titre page

st.title("StatCoop - Angélique MAIRE")

st.sidebar.markdown("Menu")

option = st.sidebar.selectbox(
    "Choisissez une option",
    ["Acceuil", "Par technicien", "Par années"]
)

if option == "Acceuil":
    st.write("Choisir un filtre")

elif option == "Par technicien":
    st.write("Statistiques par technicien")

    st.sidebar.markdown("Filtres")

    filtre = st.sidebar.selectbox(
        "Choisissez un filtre",
        ["Aucun","famille n°40","famille n°41","famille n°42","famille n°43","famille n°44","famille n°45","famille n°46"]
    )


# chagrement SQL
    
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT *
        FROM {dbschema}.{dbtable}
    """)

    df = pd.DataFrame(
        cursor.fetchall(),
        columns=[desc[0] for desc in cursor.description]
    )

    cursor.close()


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
        .format({
            "2024-2025": "{:.2f}",
            "2025-2026": "{:.2f}",
            "evolution_%": "{:.2f}%"
        })
        .map(
            color_evolution,
            subset=["evolution_%"]
        ),
        hide_index=True
    )

# Fermeture connexion
    conn.close()


#Autre page à définir

elif option == "Par années":
    st.write(''':rainbow[:construction: EN CONSTRUCTION :construction:]''')
