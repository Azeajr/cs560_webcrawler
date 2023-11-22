from pydantic import BaseSettings

class CommonSettings(BaseSettings):
    ENV: str

class DevelopmentSettings(CommonSettings):
    pass

class TestingSettings(CommonSettings):
    pass
class ProductionSettings(CommonSettings):
    pass

def get_settings():
    config = CommonSettings()
    match config.ENV:
        case "dev":
            return DevelopmentSettings()
        case "test":
            return TestingSettings()
        case "prod":
            return ProductionSettings()
        case _:
            raise ValueError(f"Invalid environment {config.ENV}.")