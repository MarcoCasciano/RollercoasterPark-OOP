from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = {"env_file": ".env"}

    app_name: str = "Rollercoaster API"
    debug: bool = True
    database_url: str

settings = Settings()
