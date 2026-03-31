from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class code_input(BaseModel):
    code: str


@app.get("/")
def home():
    return{
        "message": "Welcome to backend",
    }

@app.post("/debug")
def debug(data: code_input):
    result = data.code

    if( "print('"in result and not result.endswith("')")):
        return {
            "error": "Syntax Error",
            "explanation": "Looks like you forgot to close the quote or bracket.",
            "fixed_code": "print('Hello')"
        }
    
    return{
        "message" :"Its Working!!",
        "your code": result
    }


