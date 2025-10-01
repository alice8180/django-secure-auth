REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "accounts.csrf_authentication.CsrfAuthentication", # csrf authentication
        "accounts.authentication.CookieJWTAuth", # cookie base authentication
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
         "accounts.permissions.IsOwner", # sudhu owner tar nijer shobkisu CRUD korte parbe
    ),
    
    # for API AutoDocs  
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"
}