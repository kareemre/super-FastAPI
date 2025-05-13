#handle both success and error responses
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class CustomApiSuccessResponse(JSONResponse):
    """
    Custom API response class to handle both success and error responses.
    """
   
    def render(self, content: dict) -> bytes:
        
        custom_content = {
            "payload": content,
            "success": True,
            "errors": None,
        }
        
        return super().render(custom_content)

async def custom_validation_exception_handler(request, exc, status_code=422):
    """
    Custom exception handler for validation errors.
    
    Args:
        request: The request object.
        exc (RequestValidationError): The validation error exception.
    
    Returns:
        JSONResponse: A JSON response with the error details.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "payload": None,
            "message": "Validation Error",
            "errors": exc.errors(),
        }
    )