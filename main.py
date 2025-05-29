from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router
import uvicorn

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes from router.py
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Welcome to Job Finder API!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
