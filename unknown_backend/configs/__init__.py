from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "dev"

    rdb_username: str = "crowdworks"
    rdb_password: str = "crowdworks"
    rdb_hostname: str = "crowdworks.ap-northeast-2.rds.amazonaws.com"
    rdb_db_name: str = "CrowdWorks"

    SQLALCHEMY_DATABASE_URL: str = "sqlite+aiosqlite:////tmp/sqlite3.db"

    BACKEND_HOST: str = f"https://unknown-dev.internal.oheadline.com"


settings = Settings()
