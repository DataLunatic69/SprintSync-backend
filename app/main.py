from fastapi import FastAPI, Request
from app.database import engine
from app.models import Base
from app.router import auth, tasks, ai, users
from app.exceptions import register_all_errors
import logging
import time
from jose import JWTError, jwt
from app.config import config
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SprintSync API", version="1.0.0")

# Register all exception handlers
register_all_errors(app)

# Create tables (Alembic handles this, but good for development)
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(ai.router)
app.include_router(users.router)

origins = [
    "http://localhost:3000",  # Local development
    "https://your-frontend-domain.vercel.app", 
    "https://sprintsync-backend.onrender.com", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Try to get user ID from token
    user_id = "anonymous"
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
            user_id = payload.get("sub", "anonymous")
        except JWTError:
            pass  # Keep as anonymous if token is invalid
    
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    logger.info(
        f"Method={request.method} "
        f"Path={request.url.path} "
        f"Status={response.status_code} "
        f"UserID={user_id} "
        f"Latency={process_time:.2f}ms"
    )
    
    return response

@app.get("/")
def read_root():
    return {"message": "SprintSync API is running!"}