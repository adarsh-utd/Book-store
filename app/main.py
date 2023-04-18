import uvicorn as uvicorn
from fastapi import FastAPI

from app.router import auth

app = FastAPI()
app.include_router(auth.router)

if __name__ == '__main__':
    uvicorn.run(app=app, host='localhost', port=8000)