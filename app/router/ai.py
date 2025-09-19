from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_active_user
from app import schemas
from app.config import config
import logging
from langchain_groq import ChatGroq

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/suggest")
async def suggest_task_description(
    request: schemas.TaskBase,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.info(f"AI suggest request from user {current_user.username} for task: '{request.title}'")
    
    api_key = config.GROQ_API_KEY
    
    if not api_key:
        logger.warning("GROQ_API_KEY not configured, using fallback implementation")
        # Better fallback with structure
        fallback_description = f"""**Objective**: Complete {request.title}

**Key Requirements**:
- Define clear acceptance criteria
- Ensure proper testing coverage
- Document implementation details

**Estimated Time**: 2-4 hours

**Priority**: Medium"""
        return {"description": fallback_description}
    
    try:
        chat = ChatGroq(
            model_name=config.GROQ_MODEL,
            groq_api_key=api_key
        )
        
        # Much better prompt for structured output
        prompt = f"""Generate a concise, well-structured task description for: "{request.title}"

Format the response as follows:
- Start with a brief 1-2 sentence overview
- Include 3-5 bullet points of key requirements or steps
- Keep total response under 150 words
- Use clear, actionable language
- Do not include markdown headers or excessive formatting

Task title: {request.title}"""
        
        logger.info(f"Sending structured prompt to AI")
        
        response = chat.invoke(prompt)
        ai_description = response.content.strip()
        
        # Clean up any excessive formatting
        ai_description = ai_description.replace("**", "").replace("##", "")
        
        # Ensure it's not too long
        if len(ai_description) > 500:
            ai_description = ai_description[:497] + "..."
        
        logger.info(f"AI response received: {len(ai_description)} characters")
        
        return {"description": ai_description}
        
    except Exception as e:
        logger.error(f"Error generating AI description: {str(e)}", exc_info=True)
        # Return a simple fallback instead of error
        return {
            "description": f"Implement and test {request.title}. Ensure all requirements are met and code is properly documented."
        }