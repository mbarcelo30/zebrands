from .common import *

DEBUG = False
TEST_RUNNER = "django.test.runner.DiscoverRunner"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
