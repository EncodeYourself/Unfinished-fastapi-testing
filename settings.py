from pydantic import BaseSettings

class System_variables(BaseSettings):
    db_hostname: str
    db_port: str
    db_password: str
    db_name: str
    db_username: str
    secret_key: str
    algorithm: str
    token_duration: int

    class Config:
        env_file = '.env'

settings = System_variables()