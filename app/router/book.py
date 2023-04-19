from bson import ObjectId
from fastapi import APIRouter, Depends
from starlette import status

from app.core.config import settings
from app.db.base import books_collection, favourite_books_collection
from app.models.books import BookRequestModel, Books, LikeDislike, BookUpdateRequestModel
from app.utils.utils import get_error_response, get_current_active_user, get_book_cache, get_books_from_mongodb

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
    settings.redis_instance.delete('books')
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
    books = get_book_cache()
    find_query = {
        "is_deleted": False
    }
    if books is None:
        books = get_books_from_mongodb(find_query)
    response = {
        "books": books
    }
    return response


@router.post('/add-remove-favourite-books/{book_id}')
async def add_remove_favourite_books(book_id: str,
                                     like_dislike: LikeDislike,
                                     user: object = Depends(get_current_active_user)):
    find_favorite_books_query = {
        "customer_id": user.get("_id")
    }
    favourite_books = favourite_books_collection.find_one(find_favorite_books_query)
    response = {
        "status": True
    }
    if favourite_books is None:
        add_favourite_book = {
            "customer_id": user.get("_id"),
            "favourite_books_list": book_id
        }
        favourite_books_collection.insert_one(add_favourite_book)
        response['message'] = 'added favourite book'
    else:
        favourite_books_list = favourite_books.get('favourite_books_list')
        favourite_books_list = favourite_books_list.split(',')
        if like_dislike == LikeDislike.like:
            if book_id not in favourite_books_list:
                favourite_books_list.append(book_id)
                update = {
                    "favourite_books_list": ','.join(favourite_books_list)
                }
                favourite_books_collection.update_one(find_favorite_books_query, {"$set": update})
                response['message'] = 'added favourite book'
        if like_dislike == LikeDislike.dislike:
            if book_id not in favourite_books_list:
                return get_error_response("Bad request",
                                          status.HTTP_400_BAD_REQUEST)
            favourite_books_list.remove(book_id)
            update = {
                "favourite_books_list": ','.join(favourite_books_list)
            }
            favourite_books_collection.update_one(find_favorite_books_query, {"$set": update})
            response['message'] = 'Disliked'

    return response


@router.get('/view-favourite-books/{customer_id}')
async def get_favourite_books(customer_id: str, user: object = Depends(get_current_active_user)):
    find_favorite_books_query = {
        "customer_id": ObjectId(customer_id)
    }
    favourite_books = favourite_books_collection.find_one(find_favorite_books_query)
    favourite_books_id_list = favourite_books.get("favourite_books_list").split(',')
    book_list = list(books_collection.find({"is_deleted": False}))
    favourite_book_list = [next((Books(**a).list_books() for a in book_list if a.get("_id") == ObjectId(book_id)), None)
                           for book_id in favourite_books_id_list]
    response = {
        "favourite_book_list": favourite_book_list
    }
    return response


@router.put('/update-book/{book_id}')
async def update_book(book_id: str, request: BookUpdateRequestModel, user: object = Depends(get_current_active_user)):
    find_query = {
        "_id": ObjectId(book_id)
    }
    book = books_collection.find_one(find_query)
    if book is None:
        return get_error_response("Book not found",
                                  status.HTTP_404_NOT_FOUND)
    update = {
        "name": request.name,
        "description": request.description,
        "image": request.image,
    }
    books_collection.update_one(find_query, {"$set": update})
    settings.redis_instance.delete('books')
    response = {
        "status": True,
        "message": "updated"
    }
    return response
