from fastapi import FastAPI
from routes import router  # this is your APIRouter from routes.py

app = FastAPI(title="Bank Service PoC with MongoDB")

# include your router from routes.py
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to Bank Service PoC (MongoDB)"}
