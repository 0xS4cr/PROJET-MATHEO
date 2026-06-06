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
    ["Acceuil", "Par domaines", "Par années"]
)

if option == "Acceuil":
    st.write("Choisir un filtre")
elif option == "Par domaines":
    st.write("Hello world")
elif option == "Par années":
    st.write("Hello world")
