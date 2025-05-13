from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):  
    """Database settings configuration for the application."""
    db_connection: str
    db_host: str = "localhost"
    db_port: int 
    db_name: str 
    db_user: str
    db_password: str
    
    #reading from .env file
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
    )
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from components."""
        return f"{self.db_connection}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"