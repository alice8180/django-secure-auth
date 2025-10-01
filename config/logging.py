import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Create logs directory if not exists





LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

PROJECT_DIR = (LOG_DIR / "project")
PROJECT_DIR.mkdir(exist_ok=True)

ACCOUNTS_DIR = (LOG_DIR / "accounts")
ACCOUNTS_DIR.mkdir(exist_ok=True)

UTILS_DIR = (LOG_DIR / "utils")
UTILS_DIR.mkdir(exist_ok=True)

"""Default Handlers Value"""
# ata holo file ar default value
FILE = {
    "level": "INFO",
    "class": "logging.handlers.RotatingFileHandler",
    # "filename": <logger specific path>
    "maxBytes": 5 * 1024 * 1024,  # প্রতি 5MB হলে rotate
    "backupCount": 5,             # ৫টা পুরোনো log রাখবে
    "formatter": "verbose",
    
}

# ata holo error file ar default value
ERROR_FILE = {
    "level": "ERROR",
    "class": "logging.handlers.RotatingFileHandler",
    # "filename": < akhne log file ar path dite hobe>
    "maxBytes": 5 * 1024 * 1024,
    "backupCount": 5,
    "formatter": "verbose",
}




"""Default Loggers Value"""
LOGGERS_INFO = {
    "level": "INFO",
    "propagate": False,
}




# configure logging hare 
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    # 🔹 Formatters → কেমন format এ log show হবে
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] - %(message)s",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_white,bg_red",
            },
        },
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] - %(message)s",
        },
    },

    # 🔹 Handlers → কোথায় log যাবে
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
        
        
        "file": {
            **FILE,
            "filename": str(LOG_DIR / "project/project.log"),
        },
        "error_file": {
            **ERROR_FILE,
            "filename": str(LOG_DIR / "project/errors.log"),
        },
        
        
        # apps logger
        "accounts_file": {
            **FILE,
            "filename": str(LOG_DIR / "accounts/accounts.log"),
        },
        "accounts_error_file": {
            **ERROR_FILE,
            "filename": str(LOG_DIR / "accounts/errors.log"),
        },
        
        
        "utils_file": {
            **FILE,
            "filename": str(LOG_DIR / "utils/utils.log"),
        },
        "utils_error_file": {
            **ERROR_FILE,
            "filename": str(LOG_DIR / "utils/errors.log")
        }
    },



    # 🔹 Loggers → কোন app এর log কেমন হবে
    "loggers": {
        "django": {   # Django default logs
            "handlers": ["console", "file", "error_file"],
            "level": "INFO",
            "propagate": True,
        },
        "project": {  # তোমার project-specific log
            "handlers": ["console", "file", "error_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        # apps        
        "accounts": {  
            "handlers": ["console", "accounts_file", "accounts_error_file"],
            **LOGGERS_INFO,
        },
        
        "utils": {
            "handlers": ["console", "utils_file", "utils_error_file"],
            **LOGGERS_INFO,
        }
        
    },
}
