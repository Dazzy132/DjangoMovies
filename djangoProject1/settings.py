import os.path
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv("DEBUG", default=False) == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

INSTALLED_APPS = [
    # Мультиязычность - pip install django-modeltranslation
    'modeltranslation',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Приложение для создания простых страниц
    'django.contrib.sites',
    'django.contrib.flatpages',

    # pip install django-ckeditor
    'ckeditor',
    'ckeditor_uploader',

    # Регистрация приложений
    'movies.apps.MoviesConfig',
    'contact.apps.ContactConfig',

    # Регистрация рекаптчи
    'snowpenguin.django.recaptcha3',

    # Аутентификация - pip install django-allauth
    'allauth',
    'allauth.account',
    # Подключить регистрацию по ВК
    'allauth.socialaccount',
    'allauth.socialaccount.providers.vk',
    # https://vk.com/dev - регистрация приложения.

    'crispy_forms'
]

# Для работы с авторизацией нужно проверить
# 1) 'django.contrib.auth' и django.contrib.sites в INSTALLED_APPS
# 2) Объявлена переменная SITE_ID = 1
# 3) Так же указать переменную AUTHENTICATION_BACKENDS

# Для работы с FlatPages нужно дополнительно проверить что в Middleware есть
# 'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Подключение простых страниц
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # Подключение мультиязычности
    'django.middleware.locale.LocaleMiddleware',
]

# Настройка для работы с IFrame
X_FRAME_OPTIONS = 'SAMEORIGIN'

ROOT_URLCONF = 'djangoProject1.urls'
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoProject1.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ------- Для авторизации (django-allauth) ---------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1  # Кол-во дней для подтверждения email
ACCOUNT_USERNAME_MIN_LENGTH = 4  # Минимальное кол-во символов пользователя

# Работа с почтой: https://django-allauth.readthedocs.io/en/latest/configuration.html
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'  # email крутится в консоли.
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')  # Папка хранения email сообщений
# ------------ Авторизация ------------------------------

if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []
else:
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True  # Проверяем True ли. Для мультиязычности
USE_TZ = True

# ---------------- Мультиязычность ----------------------
# Для мультиязычности. Кортежем передаем языки, для которых она нужна
gettext = lambda s: s
LANGUAGES = (
    ('ru', gettext('Russia')),
    ('en', gettext('English')),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)
# ---------------- Мультиязычность ----------------------

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'movies/static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --------------- CKEDITOR ---------------
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        # 'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'

        ]),
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------- Каптча -----------
# https://www.google.com/recaptcha/admin/
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_DEFAULT_ACTION = 'generic'
RECAPTCHA_SCORE_THRESHOLD = 0.5
# ---------- Каптча -----------

# Для работы авторизации + простых страниц
SITE_ID = 3  # Todo: Change 1

CRISPY_TEMPLATE_PACK = 'bootstrap4'