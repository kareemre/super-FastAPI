from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from app.database.connection.connection import sessionmanager

from app.routers.routes_registry import register_routes
from app.routers.api_response.custom_api_response import custom_validation_exception_handler

app = FastAPI(debug=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()

#register application routes
register_routes(app, prefix="/api/v1")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    Custom exception handler for validation errors.
    
    Args:
        request: The request object.
        exc (RequestValidationError): The validation error exception.
    
    Returns:
        JSONResponse: A JSON response with the error details.
    """
    return await custom_validation_exception_handler(request, exc)

