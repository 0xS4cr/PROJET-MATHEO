import os

import altair as alt
import pandas as pd
import streamlit as st
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config import settings
from database import Base, SessionLocal, engine


st.set_page_config(page_title=settings.streamlit_title, layout="wide")
st.title(settings.streamlit_title)

st.sidebar.header("Configuration")
if st.sidebar.button("Vérifier la connexion DB"):
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.scalar()
            st.success(f"Connexion réussie : {version}")
    except SQLAlchemyError as error:
        st.error(f"Erreur de connexion : {error}")

st.markdown("## Exemple de tableau de données")

sample_data = pd.DataFrame(
    {
        "Nom": ["Alice", "Bob", "Matheo", "Chloé"],
        "Score": [88, 92, 75, 81],
        "Ville": ["Paris", "Lyon", "Nantes", "Bordeaux"],
    }
)

st.dataframe(sample_data)

chart = alt.Chart(sample_data).mark_bar().encode(
    x=alt.X("Nom", sort=None),
    y="Score",
    color="Ville",
)

st.altair_chart(chart, use_container_width=True)

st.sidebar.markdown("### Actions")
if st.sidebar.button("Créer les tables SQLAlchemy"):
    try:
        Base.metadata.create_all(bind=engine)
        st.success("Tables créées avec succès.")
    except SQLAlchemyError as error:
        st.error(f"Erreur de création des tables : {error}")

st.sidebar.info("Modifiez `config.py` et `.env` pour adapter la configuration PostgreSQL.")
