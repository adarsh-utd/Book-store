from fastapi import APIRouter, Depends
from starlette import status

from app.db.base import customers_collection, favourite_books_collection
from app.models.customers import CustomerModel
from app.utils.utils import get_current_active_user, get_error_response

router = APIRouter(
    prefix="/customer",
    tags=["Customer"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.get('/customer-list')
async def customer_list(user: object = Depends(get_current_active_user)):
    find_query = {
        "is_deleted": False
    }
    if user is None:
        return get_error_response("Unauthorized",
                                  status.HTTP_401_UNAUTHORIZED)
    customers_list = list(customers_collection.find(find_query))
    customers = [CustomerModel(**x).customer_list_response() for x in customers_list]
    response = {
        "customers": customers
    }
    return response


@router.get('/customers-with-favorite-books')
async def get_customers_with_favourite_books_count(user: object = Depends(get_current_active_user)):
    find_query = {
        "is_deleted": False
    }
    customers_list = list(customers_collection.find(find_query))

    favourite_books = list(favourite_books_collection.find())
    customers_response_list = []
    for customer in customers_list:
        favourite_book = next((a.get("favourite_books_list") for a in favourite_books
                               if a.get('customer_id') == customer.get('_id')), None)
        customer_response = CustomerModel(**customer).customer_list_response()
        customer_response['favourite_book_count'] = len(favourite_book.split(','))
        customers_response_list.append(customer_response)
    response = {
        "customer_response": customers_response_list
    }
    return response
