from rest_framework.exceptions import APIException

class CustomerNotFoundException(APIException):
    status_code = 404
    default_detail = "Customer not found."
    default_code = "customer_not_found"

class InvalidDataException(APIException):
    status_code = 400
    default_detail = "Invalid data provided."
    default_code = "invalid_data"

class InternalServerException(APIException):
    status_code = 500
    default_detail = "An unexpected error occurred. Please try again later."
    default_code = "internal_server_error"

class NotFoundException(APIException):
    status_code = 404
    default_detail = "Resource not found."
    default_code = "not_found"

class PermissionDeniedException(APIException):
    status_code = 403
    default_detail = "You do not have permission to perform this action."
    default_code = "permission_denied"

class ThrottledException(APIException):
    status_code = 429
    default_detail = "Too many requests. Please try again later."
    default_code = "throttled"

class ConflictException(APIException):
    status_code = 409
    default_detail = "Conflict occurred with the current state of the resource."
    default_code = "conflict"

class BadRequestException(APIException):
    status_code = 400
    default_detail = "Bad request. Please check your input data."
    default_code = "bad_request"
