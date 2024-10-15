import logging.config
from fastapi import FastAPI
from gutenberg_app.routers.router_gutenberg import router as gutenberg_router

# setup loggers
logging.config.fileConfig('config/logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger('gutenberg_app')

app = FastAPI()
app.include_router(gutenberg_router, prefix="/v1")
