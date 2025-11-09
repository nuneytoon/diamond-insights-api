from fastapi import FastAPI
from app.api.routes import health, sports

app = FastAPI(title="Diamond Insights API", description="API for the Diamond Insights project")

app.include_router(health.router)
app.include_router(sports.router)

@app.get("/")
def root():
    return {"message": "Welcome to Diamond Insights!"}
