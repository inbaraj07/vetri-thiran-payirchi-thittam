from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
BASE_DIR=Path(__file__).resolve().parent.parent
class Settings(BaseSettings):
    app_name:str=Field(default='PocketSmart AI',alias='APP_NAME')
    app_env:str=Field(default='development',alias='APP_ENV')
    secret_key:str=Field(default='change-me',alias='SECRET_KEY')
    database_path:str=Field(default='data/pocketsmart.db',alias='DATABASE_PATH')
    gemini_api_key:str|None=Field(default=None,alias='GEMINI_API_KEY')
    gemini_model:str=Field(default='gemini-2.5-flash',alias='GEMINI_MODEL')
    access_token_expire_minutes:int=Field(default=1440,alias='ACCESS_TOKEN_EXPIRE_MINUTES')
    max_upload_mb:int=Field(default=5,alias='MAX_UPLOAD_MB')
    frontend_origins:str=Field(default='http://127.0.0.1:8000,http://localhost:8000',alias='FRONTEND_ORIGINS')
    model_config=SettingsConfigDict(env_file='.env',env_file_encoding='utf-8',extra='ignore')
    @property
    def db_file(self):
        p=Path(self.database_path); return p if p.is_absolute() else BASE_DIR/p
    @property
    def origins(self): return [x.strip() for x in self.frontend_origins.split(',') if x.strip()]
@lru_cache
def get_settings(): return Settings()
