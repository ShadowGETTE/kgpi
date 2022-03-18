import os

DEBUG = os.environ.get("DEBUG", "true") in ["true", "on"]
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ["POSTGRES_DB"],
        'USER': os.environ["POSTGRES_USER"],
        'PASSWORD': os.environ["POSTGRES_PASSWORD"],
        'HOST': os.environ["POSTGRES_HOST"],
    }
}
