from fastapi import Depends, FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.routers import events, health, auth
from app.middleware.logging import LoggingMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Logging Middleware
app.add_middleware(LoggingMiddleware)

app.include_router(events.router)
app.include_router(health.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello Events Applications!"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)



