from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    POSTGRES_DSN: str
    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_PORT: str


settings = Settings()
