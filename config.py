import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    database_url: str = os.getenv("A RENSEIGNER")
    streamlit_title: str = os.getenv("STREAMLIT_TITLE", "Projet Matheo")


settings = Settings()
