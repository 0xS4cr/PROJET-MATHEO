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

conn = psycopg2.connect(
    host=host,
    database=dbname,
    user=user,
    password=password
)


#Titre page

st.title("StatCoop - Angélique MAIRE")

st.sidebar.title("Menu")

option = st.sidebar.selectbox(
    "Choisissez une option",
    ["Acceuil", "Par technicien", "Par années"]
)

if option == "Acceuil":
    st.write("Choisir un filtre")

elif option == "Par technicien":
    st.write("Statistiques par technicien")


    #deuxième menu dans la side bar
    st.sidebar.title("Filtres")

    filtre = st.sidebar.selectbox(
        "Choisissez un filtre",
        ["Aucun","famille n°40","famille n°41","famille n°42","famille n°43","famille n°44","famille n°45","famille n°46"]
    )


    # Affichage du tableau sans filtre.

    if filtre =="Aucun":

        #Définition du curseur pour le tableau SQL
        cursor = conn.cursor()

    # je défini df pour l'utiliser dans mon filtrage
        cursor.execute(f"""
            SELECT *
            FROM {dbschema}.{dbtable}
        """)

        filtre = cursor.fetchall()

        df = pd.DataFrame(
            filtre,
            columns=[desc[0] for desc in cursor.description]
        )

        df["date_operation"] = pd.to_datetime(df["date_operation"])
        df["quantite"] = pd.to_numeric(df["quantite"], errors="coerce")

        # création colonne année
        df["annee"] = df["date_operation"].dt.year

        # tableau croisé
        df_table = pd.pivot_table(
            df,
            index=["technicien", "annee"],
            columns= "code_famille",
            values="quantite",
            aggfunc="sum",
            fill_value=0
        )
        df_table = df_table.reset_index()
        # on masque les doublons de technicien
        df_table["technicien_affiche"] = df_table["technicien"].mask(
        df_table["technicien"].duplicated()
        )

        # on remplace la colonne pour affichage
        df_table["technicien"] = df_table["technicien_affiche"]
        df_table = df_table.drop(columns=["technicien_affiche"])

        st.dataframe(df_table, hide_index=True)


        #Fermeture du curseur et de la connexion SQL
        cursor.close()
        conn.close()



    elif filtre == "famille n°40":
         
        cursor = conn.cursor()

    # je défini df pour l'utiliser dans mon filtrage
        cursor.execute(f"""
            SELECT *
            FROM {dbschema}.{dbtable}
        """)

        filtre = cursor.fetchall()

        df = pd.DataFrame(
            filtre,
            columns=[desc[0] for desc in cursor.description]
        )
        
        df["annee"] = df["date_operation"].dt.year
        df["date_operation"] = pd.to_datetime(df["date_operation"])
        df["annee"] = df["date_operation"].dt.year

        df["quantite"] = pd.to_numeric(df["quantite"], errors="coerce")

        # label affichage
        df["famille_affichage"] = df["code_famille"].astype(str)

        df.loc[
            df["code_famille"] == 40,
            "famille_affichage"
        ] = df["famille_2"]

        # pivot
        df_table = pd.pivot_table(
            df,
            index=["technicien", "annee"],
            columns="famille_affichage",
            values="quantite",
            aggfunc="sum",
            fill_value=0
        )

        # masquer doublons technicien (affichage propre)
        df_table = df_table.reset_index()

        df_table["technicien_affiche"] = df_table["technicien"].mask(
            df_table["technicien"].duplicated()
        )

        df_table["technicien"] = df_table["technicien_affiche"]
        df_table = df_table.drop(columns=["technicien_affiche"])

        st.dataframe(df_table, hide_index=True)

        #Fermeture du curseur et de la connexion SQL
        cursor.close()
        conn.close()




elif option == "Par années":
    st.write(''':rainbow[EN CONSTRUCTION]''')


