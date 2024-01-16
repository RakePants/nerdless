from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: int = 5432
    database_password: str
    database_name: str
    database_username: str

    port: int = 5000
    telegram_token: str
    mode: str = 'polling'
    webhook_url: str = ""
    log_level: str = 'INFO'

    lm_mode: str = 'local'
    hf_model_name: str

    class Config:
        extra = 'ignore'


settings = Settings()
