from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.database.connection.sql_connection import create_db_and_tables
from app.routers.routes_registry import register_routes
from app.routers.api_response.custom_api_response import custom_validation_exception_handler

app = FastAPI(debug=True)


@app.on_event("startup")
async def on_startup():
    """Create database tables on startup."""
    
    create_db_and_tables()
    print("Database tables created!")

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

