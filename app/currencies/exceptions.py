from fastapi import HTTPException, status


class CustomException(HTTPException):
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class CurrencyException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Not available currencies"


class AmountException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Amount must be greater than 0"


class ReadTimeOutException(CustomException):
    status_code = status.HTTP_504_GATEWAY_TIMEOUT
    detail = "Request timeout"


class RequestException(CustomException):
    status_code = status.HTTP_502_BAD_GATEWAY
    detail = "Failed to make request"
