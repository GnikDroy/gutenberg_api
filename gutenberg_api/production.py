import os
from .settings import *

DEBUG = False

STATIC_ROOT = os.getenv("STATIC_ROOT")

SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = list(filter(None, (os.getenv('ALLOWED_HOSTS') or '').split(";"))) 

SECURE_BROWSER_XSS_FILTER = True