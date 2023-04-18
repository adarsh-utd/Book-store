from fastapi import APIRouter, Depends
from starlette import status

from app.db.base import customers_collection
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
