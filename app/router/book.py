from fastapi import APIRouter, Depends
from starlette import status

from app.db.base import books_collection
from app.models.books import BookRequestModel, Books
from app.utils.utils import get_error_response, get_current_active_user

router = APIRouter(
    prefix="/book",
    tags=["Books"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post('/create-book')
async def create_book(request: BookRequestModel, user: object = Depends(get_current_active_user)):
    if user is None:
        return get_error_response("Unauthorized",
                                  status.HTTP_401_UNAUTHORIZED)
    book = {
        "name": request.name,
        "description": request.description,
        "is_deleted": False
    }

    if request.image is not None:
        book['image'] = request.image

    books_collection.insert_one(book)
    response = {
        "status": True,
        "message": 'Book added'
    }
    return response


@router.get('/list-books')
async def list_books(user: object = Depends(get_current_active_user)):
    if user is None:
        return get_error_response("Unauthorized",
                                  status.HTTP_401_UNAUTHORIZED)

    find_query = {
        "is_deleted": False
    }
    book_list = list(books_collection.find(find_query))
    books = [Books(**x).list_books() for x in book_list]

    response = {
        "books": books
    }
    return response