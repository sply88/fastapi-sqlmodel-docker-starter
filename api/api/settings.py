from pydantic import BaseSettings


class Settings(BaseSettings):
    db_uri: str
