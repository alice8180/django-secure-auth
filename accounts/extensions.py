from drf_spectacular.extensions import OpenApiAuthenticationExtension


# create your extensions


class CsrfAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'accounts.csrf_authentication.CsrfAuthentication'
    name = 'CsrfAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-CSRFToken',   # তোমার CSRF header এর নাম
            'description': 'CSRF protection token'
        }



class CookieJWTAuthScheme(OpenApiAuthenticationExtension):
    target_class = 'accounts.authentication.CookieJWTAuth'
    name = 'CookieJWT'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': 'access_token',  # settings.SIMPLE_JWT["AUTH_COOKIE"]
            'description': 'JWT access token stored in HttpOnly cookie'
        }


class CookieJWTRefreshAuthScheme(OpenApiAuthenticationExtension):
    target_class = 'accounts.authentication.CookieJWTAuth'
    name = 'CookieJWTRefresh'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': 'refresh_token',  # settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"]
            'description': 'JWT refresh token stored in HttpOnly cookie'
        }
