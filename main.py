from fastapi import FastAPI
from handlers.handler import router
from handlers.impianti_handler import router_impianti

app = FastAPI(

    openapi_url='/documentation/json',

    docs_url='/documentation/',

    redoc_url=None
)

app.include_router(router)
app.include_router(router_impianti)