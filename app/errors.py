from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.templating import Jinja2Templates


# load templates
templates = Jinja2Templates(directory="app/templates")


# Handle HTTPExceptions here
async def http_exceptions_handler(request: Request, exception: HTTPException) -> templates.TemplateResponse:
    return templates.TemplateResponse("error.html", {"request": request, "error_code": exception.status_code, "error_message": exception.detail, "message": ""})


# Handle RequestValidationError here
async def request_validation_error_handler(request: Request, exception: RequestValidationError) -> templates.TemplateResponse:
    return templates.TemplateResponse("error.html", {"request": request, "error_code": 422, "error_message": "RequestValidationError", "message": str(exception)})
