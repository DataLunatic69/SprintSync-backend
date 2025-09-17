from fastapi import FastAPI
from app.database import engine
from app.models import Base

app = FastAPI(title="SprintSync API", version="1.0.0")

# Create tables (Alembic handles this, but good for development)
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "SprintSync API is running!"}