import os

from decouple import config


# from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings
#
# find_dotenv()
# load_dotenv()

# class Settings(BaseSettings):
#     database_username: str = os.getenv("DATABASE_USERNAME")
#     database_password: str = os.getenv("DATABASE_PASSWORD")
#     database_hostname: str = os.getenv("DATABASE_HOSTNAME")
#     database_port: str = os.getenv("DATABASE_PORT")
#     database_name: str = os.getenv("DATABASE_NAME")
#     secret_key: str = os.getenv("SECRET_KEY")
#     algorithm: str = os.getenv("ALGORITHM")
#     access_token_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

#     class Config:
#         env_file = ".env"
#         env_file_encoding = 'utf-8'


# Retrieve the variables from the .env file
class Settings(BaseSettings):
    database_username = config('DATABASE_USERNAME')
    database_password = config('DATABASE_PASSWORD')
    database_hostname = config('DATABASE_HOSTNAME')
    database_port = config('DATABASE_PORT')
    database_name = config('DATABASE_NAME')
    secret_key = config('SECRET_KEY')
    algorithm = config('ALGORITHM')
    access_token_expire_minutes = config('ACCESS_TOKEN_EXPIRE_MINUTES')


settings = Settings()
