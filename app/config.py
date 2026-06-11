from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # This tells Pydantic: "I strictly require a string named DATABASE_URL to exist in the environment"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # This tells Pydantic to look for variables in the .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Create a global instance of the settings to use throughout the app
settings = Settings()