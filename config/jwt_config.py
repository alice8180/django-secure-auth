from datetime import timedelta

# create your JWT config hare

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "USER_ID_FIELD": "uuid", # user ke jokhon akta token deya hobe tokhon user ke ki vabe cinbe ata akta user , karon shobar tohh kono na kono unique name lagbe , tai uuid diye protita user ke alada alada kore cinbe
    "USER_ID_CLIME" : "user_id", # karon ami je user ar jonno backend a uuid use korsi seta tohh r fontend a deya jaina , tai akta shoddobeshi name 
    "BLACKLIST_AFTER_ROTATION": True,
    
    # configure jwt token 
    "AUTH_COOKIE_PATH": "/", # "/" ar mane holo jekono link ba route ar sathe cookie jabe jodi "/home" kortam tahole shudhu matro /home a user click kore cookie backend a ashto , onno kono link a click korle astona :) tai / root a rakhai bhalo 
    "AUTH_COOKIE": "access_token",
    "AUTH_COOKIE_REFRESH": "refresh_token",
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_SAMESITE" : "Lax",
    # "AUTH_COOKIE_SECURE": True, # shudhu matro https ar khetre kajj korbe 
}