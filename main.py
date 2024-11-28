from fastapi import FastAPI
from handlers.handler import router
from handlers.impianti_handler import router_impianti
from handlers.macchinari_handler import router_macchinari
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(

    openapi_url='/documentation/json',

    docs_url='/documentation/',

    redoc_url=None
)

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

app.include_router(router)
app.include_router(router_impianti)
app.include_router(router_macchinari)