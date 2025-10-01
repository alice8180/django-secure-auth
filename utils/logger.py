import logging
from typing import Optional
from django.http import HttpRequest



# create your UserLogger hare

"""
Logger a akta update dite hobe , akhon logger request, user input hishebe cai kintu aktake automate kora jai
- jodi amra akta middleware banai jekhane jekono user request kolei tar request object ke dhore rakhbo 
- r request.user kore user o peyejabo tahole r protita logger ar moddhe (request=request, user=user) korte hobena
"""

class UserLogger:
    """
    Flexible logger for Django apps.
    Handles request info and user info safely.
    """

    def __init__(self, logger: object, message: str, request: Optional[HttpRequest] = None, user: Optional[object] = None):
        if isinstance(logger, str):
            # যদি string দাও, automatic getLogger ব্যবহার করবে
            self.logger = logging.getLogger(logger)
        else:
            self.logger = logger
        self.message = message
        self.request = request
        self.user = user

    def get_ip(self) -> str:
        if not self.request:
            return "Unknown"
        return (
            self.request.META.get("HTTP_X_FORWARDED_FOR")
            or self.request.META.get("REMOTE_ADDR")
            or "Unknown"
        )

    def _build_message(self) -> str:
        parts = [self.message]

        if self.user:
            if hasattr(self.user, "email"):
                parts.append(f"name: {getattr(self.user, 'first_name', '')}-{getattr(self.user, 'last_name', '')}")
                parts.append(f"email: {getattr(self.user, 'email', '')}")
            else:
                parts.append(f"user: {str(self.user)}")

        if self.request:
            parts.append(f"ip: {self.get_ip()}")

        return " | ".join(parts)



    # Logging Methods
    def log_debug(self):
        self.logger.debug(self._build_message())

    def log_info(self):
        self.logger.info(self._build_message())

    def log_warning(self):
        self.logger.warning(self._build_message())

    def log_error(self):
        self.logger.error(self._build_message())



# Helper Functions


# accounts
def accounts_log_debug(message: str, request: Optional[HttpRequest] = None, user: Optional[object] = None, app: str = "accounts"):
    UserLogger(logger=app, message=message, request=request, user=user).log_debug()

def accounts_log_info(message: str, request: Optional[HttpRequest] = None, user: Optional[object] = None, app: str = "accounts"):
    UserLogger(logger=app, message=message, request=request, user=user).log_info()

def accounts_log_warning(message: str, request: Optional[HttpRequest] = None, user: Optional[object] = None, app: str = "accounts"):
    UserLogger(logger=app, message=message, request=request, user=user).log_warning()

def accounts_log_error(message: str, request: Optional[HttpRequest] = None, user: Optional[object] = None, app: str = "accounts"):
    UserLogger(logger=app, message=message, request=request, user=user).log_error()



# utils
def utils_log_debug(message: str, request: Optional[HttpRequest] = None, user: Optional[object] = None, app: str = "utils"):
    UserLogger(logger=app, message=message, request=request, user=user).log_debug()

def utils_log_info(message: str, request: Optional[HttpRequest] = None, user: Optional[object] = None, app: str = "utils"):
    UserLogger(logger=app, message=message, request=request, user=user).log_info()

def utils_log_warning(message: str, request: Optional[HttpRequest] = None, user: Optional[object] = None, app: str = "utils"):
    UserLogger(logger=app, message=message, request=request, user=user).log_warning()

def utils_log_error(message: str, request: Optional[HttpRequest] = None, user: Optional[object] = None, app: str = "utils"):
    UserLogger(logger=app, message=message, request=request, user=user).log_error()
