from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/facturacion")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    TEMPLATES_DIR: str = "templates"
    PDF_OUTPUT_DIR: str = "generated_pdfs"

settings = Settings() 