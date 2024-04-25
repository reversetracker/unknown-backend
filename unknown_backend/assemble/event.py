import logging.config

from unknown_backend import database
from unknown_backend import models
from unknown_backend.configs import settings as default_settings

logger = logging.getLogger(__name__)


async def startup_event_1():
    logger.info(f"Default Params:")
    for key, value in default_settings.dict().items():
        logger.info(f"  {key}: {value}")


async def startup_event_2():
    logger.info("Synchronizing databases..")
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def shutdown_event():
    logger.info("shutting down..")
    await database.engine.dispose()
