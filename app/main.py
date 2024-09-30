from fastapi import Depends, FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.routers import events, health

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

app.include_router(events.router)
app.include_router(health.router)


@app.get("/")
async def root():
    return {"message": "Hello Events Applications!"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)



