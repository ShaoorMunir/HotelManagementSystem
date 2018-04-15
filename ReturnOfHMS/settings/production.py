import dj_database_url

from ReturnOfHMS.settings.common import *

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)