from collections import defaultdict
from fastapi import status

class UserException(Exception):
    """ This is base class for all user based exceptions"""
    pass

class UserAlreadyExistsException(UserException):
    pass

class InvalidCredentialsException(UserException):
    pass

class UserNotFoundException(UserException):
    pass

class ExpiredTokenException(UserException):
    pass

class InvalidTokenException(UserException):
    pass

class InsufficientPermission(UserException):
    pass

class AccessTokenException(UserException):
    pass

class RefreshTokenException(UserException):
    pass

exception_details = defaultdict(dict)
exception_details[UserAlreadyExistsException] = {'status':status.HTTP_403_FORBIDDEN, 
                                  'detail':{"message": "User with email already exists",
                                            "error_code": "user_exists",}}

exception_details[InvalidCredentialsException] = {'status':status.HTTP_401_UNAUTHORIZED, 
                                  'detail':{"message": "Invalid Email Or Password",
                                            "error_code": "invalid_email_or_password",}}

exception_details[UserNotFoundException] = {'status':status.HTTP_404_NOT_FOUND, 
                                  'detail':{"message": "User Not Found",
                                            "error_code": "Invalid user id",}}

exception_details[ExpiredTokenException] = {'status':status.HTTP_401_UNAUTHORIZED, 
                                  'detail':{"message": "Token is invalid Or expired",
                                            "resolution": "Please get new token",
                                            "error_code": "invalid_token",}}

exception_details[InvalidTokenException] = {'status':status.HTTP_401_UNAUTHORIZED, 
                                  'detail':{"message": "Token is invalid Or expired",
                                            "resolution": "Please get new token",
                                            "error_code": "invalid_token",}}

exception_details[InsufficientPermission] = {'status':status.HTTP_403_FORBIDDEN, 
                                  'detail':{"message": "You are not allowed to access this resource",
                                            "error_code": "Forbidden",}}

exception_details[AccessTokenException] = {'status':status.HTTP_401_UNAUTHORIZED, 
                                  'detail':{"message": "Provide access token",
                                            "error_code": "token required",}}

exception_details[RefreshTokenException] = {'status':status.HTTP_401_UNAUTHORIZED, 
                                  'detail':{"message": "Provide refresh token",
                                            "error_code": "token required",}}
