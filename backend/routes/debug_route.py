from fastapi import APIRouter
from models.code_models import CodeInput
from services.debug_service import debug_code_logic

router = APIRouter()

@router.post("/debug")
def debug(data: CodeInput):
    return debug_code_logic(data.code) #