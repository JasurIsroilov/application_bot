from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config_reader import config


engine = create_async_engine(url=config.db_url)
sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
