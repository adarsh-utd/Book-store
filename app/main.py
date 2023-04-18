import uvicorn as uvicorn
from fastapi import FastAPI

app = FastAPI()


if __name__ == '__main__':
    uvicorn.run(app=app, host='localhost', port=8000)