import logging
from django.http import JsonResponse
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist, ValidationError

logger = logging.getLogger(__name__)

class CustomExceptionMiddleware:
    """Middleware to handle exceptions globally."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except APIException as e:
            logger.error(f"API Exception: {str(e)}")
            return JsonResponse({"error": str(e.detail)}, status=e.status_code)
        except ObjectDoesNotExist:
            logger.error("Requested object does not exist.")
            return JsonResponse({"error": "Requested resource not found."}, status=404)
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)
            return JsonResponse({"error": "Something went wrong. Please try again later."}, status=500)
