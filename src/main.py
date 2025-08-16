from fastapi import FastAPI

from api.router import router

# fast api initialization
app = FastAPI()
app.include_router(router)
