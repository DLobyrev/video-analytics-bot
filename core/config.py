from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    telegram_bot_token: str
    database_url: str = "postgresql://postgres:postgres@postgres:5432/analytics"
    hf_token: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
