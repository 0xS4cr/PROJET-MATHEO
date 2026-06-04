from config import Settings


def test_settings_default_values():
    settings = Settings()
    assert isinstance(settings.database_url, str)
    assert isinstance(settings.streamlit_title, str)
