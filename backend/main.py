from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from services.debug_service import debug_service

app = FastAPI(title="AI Code Debugger API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DebugRequest(BaseModel):
    code: str = Field(..., min_length=5, max_length=5000)
    language: str = Field(default="python")

class DebugResponse(BaseModel):
    error: str
    root_cause: str
    fixed_code: str
    best_practice: str
    confidence_score: float

@app.on_event("startup")
async def startup_event():
    """Load the model when the server starts"""
    debug_service.load_model()

@app.get("/")
def read_root():
    return {"message": "AI Code Debugger API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/debug", response_model=DebugResponse)
async def debug_code(request: DebugRequest):
    try:
        result = debug_service.debug_code(request.code, request.language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
