from fastapi import FastAPI
from app.api.routes import health

app = FastAPI(title="Diamond Insights API", description="API for the Diamond Insights project")

app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "Welcome to Diamond Insights!"}