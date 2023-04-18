import uvicorn as uvicorn
from fastapi import FastAPI

from app.router import auth, customer, book

app = FastAPI()
app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(book.router)
if __name__ == '__main__':
    uvicorn.run(app=app, host='localhost', port=8000)