from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_active_user
from app import schemas
import os
from langchain_groq import ChatGroq

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/suggest")
async def suggest_task_description(
    request: schemas.TaskBase,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        # Fallback to stub implementation
        return {"description": f"Description for: {request.title}"}
    
    try:
        chat = ChatGroq(
            model_name="mixtral-8x7b-32768",
            groq_api_key=api_key
        )
        
        prompt = f"Generate a detailed task description for a software development task titled: {request.title}"
        response = chat.invoke(prompt)
        return {"description": response.content}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating description: {str(e)}"
        )