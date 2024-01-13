from fastapi import FastAPI

from settings import get_settings


if not get_settings().DEBUG:
    app = FastAPI(docs_url=None)
else:
    app = FastAPI()
