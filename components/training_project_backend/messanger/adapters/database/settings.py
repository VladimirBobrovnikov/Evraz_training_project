from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = 'sqlite:///messanger.db'


    # Python путь к каталогу, где лежит запускатор alembic
    # (пример: <project_name>.composites:alembic)
    ALEMBIC_SCRIPT_LOCATION: str = 'messanger.adapters.database:alembic'

    # Python путь к каталогу с миграциями
    ALEMBIC_VERSION_LOCATIONS: str = 'messanger.adapters.database:migrations'

    ALEMBIC_MIGRATION_FILENAME_TEMPLATE: str = (
        '%%(year)d_'
        '%%(month).2d_'
        '%%(day).2d_'
        '%%(hour).2d_'
        '%%(minute).2d_'
        '%%(second).2d_'
        '%%(slug)s'
    )

    LOGGING_LEVEL: str = 'INFO'
    SA_LOGS: bool = False

    @property
    def LOGGING_CONFIG(self):
        config = {
            'loggers': {
                'alembic': {
                    'handlers': ['default'],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False
                }
            }
        }

        if self.SA_LOGS:
            config['loggers']['sqlalchemy'] = {
                'handlers': ['default'],
                'level': self.LOGGING_LEVEL,
                'propagate': False
            }

        return config
