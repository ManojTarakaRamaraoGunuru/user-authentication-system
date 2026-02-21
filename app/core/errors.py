from typing import Callable, Any
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from app.core.exceptions import exception_details

def create_exception_handler(
        status_code: int, 
        detail: Any
        ) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: UserException):

        return JSONResponse(content=detail, status_code=status_code)

    return exception_handler

def register_exceptions(app: FastAPI):

    for exception, detail in exception_details.items():
        app.add_exception_handler(
            exception, 
            create_exception_handler(status_code=detail['status'], detail=detail['detail'])
            )
