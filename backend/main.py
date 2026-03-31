from fastapi import FastAPI
from routes.debug_route import router

app = FastAPI()

# connects route file to main app
app.include_router(router)


@app.get("/")
def home():
    return{
        "message": "Welcome to backend",
    }

