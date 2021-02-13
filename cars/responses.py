from rest_framework.response import Response
from rest_framework import status


def bad_request_response(errors=""):
    return Response({
        "status": "fail",
        "data": errors
    }, status=status.HTTP_400_BAD_REQUEST)


def model_saved_response(model):
    return Response({
        "status": "success",
        "data": model
    }, status=status.HTTP_201_CREATED)


def server_error_response(model):
    return Response({
        "status": "fail",
        "data": model
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
