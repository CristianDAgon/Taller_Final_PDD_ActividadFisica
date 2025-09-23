from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.parsing.parser import parse_pseudocode

router = APIRouter()

class ValidateRequest(BaseModel):
    text: str

class ValidateResponse(BaseModel):
    valid: bool

@router.post("/validate", response_model=ValidateResponse)
def validate(req: ValidateRequest):
    try:
        parse_pseudocode(req.text)
        return ValidateResponse(valid=True)
    except Exception:
        return ValidateResponse(valid=False)
