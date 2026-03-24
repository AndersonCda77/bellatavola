from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Bella Tavola API"
    debug: bool = False
    version: str = "1.0.0"
    max_mesas: int = 20

    # Configuração para ler .env automaticamente
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instância única das configurações
settings = Settings()