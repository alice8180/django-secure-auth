SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
        
    "TAGS": [
        {"name": "CSRFToken", "description": "CSRFToken this api run first then other api run"},
        {"name": "Accounts", "description": "User account & authentication APIs"},
        {"name": "ForgetPassword", "description": "Any User Reset His/Har Password"},
        {"name": "Login-Logout", "description": "Login or logout user account "},
        
    ]
}
