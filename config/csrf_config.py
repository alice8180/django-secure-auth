


"""CSRF Configure"""
# CSRF_COOKIE_AGE = 60 * 60 * 24  # 1 day
CSRF_COOKIE_AGE = 60*60  # 1h
CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_HTTPONLY = False   # JavaScript থেকে access করতে চাইলে False
CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"
CSRF_USE_SESSIONS = False



