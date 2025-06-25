from fastapi import FastAPI
from dotenv import load_dotenv

from app.adapter.api.account_router import router as account_router


load_dotenv()

app = FastAPI()
app.include_router(account_router, prefix="/account", tags=["report"])
