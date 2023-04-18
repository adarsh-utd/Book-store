from datetime import timedelta

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from app.core.config import settings
from app.db.base import customers_collection
from app.models.customers import Customers, LoginResponseModel
from app.utils.utils import get_user_email, get_error_response, get_timestamp, get_hashed_password, authenticate_user, \
    create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post('/create-customer')
async def create_customer(request: Customers):
    customer_found = get_user_email(request.email)
    if customer_found:
        return get_error_response("Email already exists",
                                  status.HTTP_400_BAD_REQUEST)
    timestamp = get_timestamp()
    password = get_hashed_password(request.password)
    customer = {
        "name": request.name,
        "password": password,
        "email": request.email,
        "signed_up_ts": timestamp,
        "is_deleted":False
    }
    customers_collection.insert_one(customer)
    customer_exist = authenticate_user(request.email, request.password)
    if not customer_exist:
        return get_error_response("Customer not found",
                                  status.HTTP_404_NOT_FOUND)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': customer_exist.get("email")},
                                       expires_delta=access_token_expires)
    expiry_time = get_timestamp() + settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60 * 1000
    response = LoginResponseModel(
        id=str(customer_exist.get('_id')),
        name=customer_exist.get('name'),
        email=customer_exist.get('email'),
        access_token=access_token,
        access_token_expiry_time=expiry_time
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(response))
