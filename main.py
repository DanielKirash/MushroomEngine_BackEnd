from fastapi import FastAPI
from handlers.handler import router

app = FastAPI(

    openapi_url='/documentation/json',

    docs_url='/documentation/',

    redoc_url=None
)

app.include_router(router)