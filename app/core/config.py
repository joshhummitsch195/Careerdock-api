from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CareerDock API"
    database_url: str = "sqlite:///./careerdock.db"
    secret_key: str = "change-this-to-a-long-random-string"
    access_token_expire_minutes: int = 1440

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
