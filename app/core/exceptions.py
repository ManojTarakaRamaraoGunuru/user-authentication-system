from collections import defaultdict

class UserException(Exception):
    """ This is base class for all user based exceptions"""
    pass

class UserAlreadyExistsException(UserException):
    pass

class ExpiredTokenException(UserException):
    pass

exception_details = defaultdict(dict)
exception_details[UserAlreadyExistsException] = {'status':'status.HTTP_403_FORBIDDEN', 
                                  'detail':{"message": "User with email already exists",
                                            "error_code": "user_exists",}}
