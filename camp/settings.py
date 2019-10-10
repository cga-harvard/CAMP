# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

# Django settings for the GeoNode project.
import ast
import os
from urlparse import urlparse, urlunparse
from django.utils.translation import ugettext_lazy as _
# Load more settings from a file called local_settings.py if it exists
try:
    from camp.local_settings import *
#    from geonode.local_settings import *
except ImportError:
    from geonode.settings import *

#
# General Django development settings
#
PROJECT_NAME = 'camp'

SITE_NAME = os.getenv('SITE_NAME', " ")
SITENAME = 'camp'

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

WSGI_APPLICATION = "{}.wsgi.application".format(PROJECT_NAME)

#ALLOWED_HOSTS = ['localhost', 'django'] if os.getenv('ALLOWED_HOSTS') is None \
#    else re.split(r' *[,|:|;] *', os.getenv('ALLOWED_HOSTS'))

PROXY_ALLOWED_HOSTS += ('nominatim.openstreetmap.org',)

# AUTH_IP_WHITELIST property limits access to users/groups REST endpoints
# to only whitelisted IP addresses.
#
# Empty list means 'allow all'
#
# If you need to limit 'api' REST calls to only some specific IPs
# fill the list like below:
#
# AUTH_IP_WHITELIST = ['192.168.1.158', '192.168.1.159']
AUTH_IP_WHITELIST = []

MANAGERS = ADMINS = os.getenv('ADMINS', [])

########################
# WorldMap configuration
INSTALLED_APPS += (PROJECT_NAME,
                   'geoexplorer-worldmap',
                   'geonode_worldmap',
                   'geonode_worldmap.gazetteer',
                   'geonode_worldmap.wm_extra',
                   'geonode_worldmap.mapnotes',
                   )

from settings import TEMPLATES
TEMPLATES[0]['OPTIONS']['context_processors'].append('geonode_worldmap.context_processors.resource_urls')

GEONODE_CLIENT_LOCATION = '/static/worldmap_client/'

USE_GAZETTEER = True
GAZETTEER_DB_ALIAS = 'default'
GAZETTEER_FULLTEXTSEARCH = False
# external services to be used by the gazetteer
GAZETTEER_SERVICES = 'worldmap,geonames,nominatim'
# this is the GeoNames key which is needed by the WorldMap Gazetteer
GAZETTEER_GEONAMES_USER = os.getenv('GEONAMES_USER', 'your-key-here')
WM_COPYRIGHT_URL = "http://gis.harvard.edu/"
WM_COPYRIGHT_TEXT = "Center for Geographic Analysis"
DEFAULT_MAP_ABSTRACT = """
    <h3>The Harvard WorldMap Project</h3>
    <p>WorldMap is an open source web mapping system that is currently
    under construction. It is built to assist academic research and
    teaching as well as the general public and supports discovery,
    investigation, analysis, visualization, communication and archiving
    of multi-disciplinary, multi-source and multi-format data,
    organized spatially and temporally.</p>
"""
# these are optionals
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'your-key-here')
USE_HYPERMAP = strtobool(os.getenv('USE_HYPERMAP', 'False'))
HYPERMAP_REGISTRY_URL = os.getenv('HYPERMAP_REGISTRY_URL', 'http://localhost:8001')
SOLR_URL = os.getenv('SOLR_URL', 'http://localhost:8983/solr/hypermap/select/')
MAPPROXY_URL = os.getenv('MAPPROXY_URL', 'http://localhost:8001')
########################

# Location of url mappings
ROOT_URLCONF = os.getenv('ROOT_URLCONF', '{}.urls'.format(PROJECT_NAME))

MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(LOCAL_ROOT, "uploaded"))

STATIC_ROOT = os.getenv('STATIC_ROOT',
                        os.path.join(LOCAL_ROOT, "static_root")
                        )

# Additional directories which hold static files
# In order to use the staticfiles in camp earlier than in geonode, use insert instead of append
# STATICFILES_DIRS.append(
STATICFILES_DIRS.insert(0,
    os.path.join(LOCAL_ROOT, "static"),
)

# Location of locale files
LOCALE_PATHS = (
    os.path.join(LOCAL_ROOT, 'locale'),
    ) + LOCALE_PATHS

TEMPLATES[0]['DIRS'].insert(0, os.path.join(LOCAL_ROOT, "templates"))
loaders = TEMPLATES[0]['OPTIONS'].get('loaders') or ['django.template.loaders.filesystem.Loader','django.template.loaders.app_directories.Loader']
# loaders.insert(0, 'apptemplates.Loader')
TEMPLATES[0]['OPTIONS']['loaders'] = loaders
TEMPLATES[0].pop('APP_DIRS', None)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'dj_pagination.middleware.PaginationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
)

CLIENT_RESULTS_LIMIT = 20
API_LIMIT_PER_PAGE = 1000
FREETEXT_KEYWORDS_READONLY = False
RESOURCE_PUBLISHING = False
ADMIN_MODERATE_UPLOADS = False
GROUP_PRIVATE_RESOURCES = False
GROUP_MANDATORY_RESOURCES = False
MODIFY_TOPICCATEGORY = True
USER_MESSAGES_ALLOW_MULTIPLE_RECIPIENTS = True
DISPLAY_WMS_LINKS = True

# prevent signing up by default
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_CONFIRMATION_EMAIL = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_APPROVAL_REQUIRED = True

SOCIALACCOUNT_ADAPTER = 'geonode.people.adapters.SocialAccountAdapter'

SOCIALACCOUNT_AUTO_SIGNUP = False

# Uncomment this to enable Linkedin and Facebook login
# INSTALLED_APPS += (
#     'allauth.socialaccount.providers.linkedin_oauth2',
# )

SOCIALACCOUNT_PROVIDERS = {
    'linkedin_oauth2': {
        'SCOPE': [
            'r_emailaddress',
            'r_basicprofile',
        ],
        'PROFILE_FIELDS': [
            'emailAddress',
            'firstName',
            'headline',
            'id',
            'industry',
            'lastName',
            'pictureUrl',
            'positions',
            'publicProfileUrl',
            'location',
            'specialties',
            'summary',
        ]
    },
}

SOCIALACCOUNT_PROFILE_EXTRACTORS = {
    "linkedin_oauth2": "geonode.people.profileextractors.LinkedInExtractor",
}

# MAPs and Backgrounds

# Default preview library
LAYER_PREVIEW_LIBRARY = 'geoext'

# LAYER_PREVIEW_LIBRARY = 'leaflet'
LEAFLET_CONFIG = {
    'TILES': [
        # Find tiles at:
        # http://leaflet-extras.github.io/leaflet-providers/preview/

        # Map Quest
        ('Map Quest',
         'http://otile4.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
         'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> '
         '&mdash; Map data &copy; '
         '<a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'),
        # Stamen toner lite.
        # ('Watercolor',
        #  'http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.png',
        #  'Map tiles by <a href="http://stamen.com">Stamen Design</a>, \
        #  <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; \
        #  <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, \
        #  <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'),
        # ('Toner Lite',
        #  'http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.png',
        #  'Map tiles by <a href="http://stamen.com">Stamen Design</a>, \
        #  <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; \
        #  <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, \
        #  <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'),
    ],
    'PLUGINS': {
        'esri-leaflet': {
            'js': 'lib/js/esri-leaflet.js',
            'auto-include': True,
        },
        'leaflet-fullscreen': {
            'css': 'lib/css/leaflet.fullscreen.css',
            'js': 'lib/js/Leaflet.fullscreen.min.js',
            'auto-include': True,
        },
    },
    'SRID': 3857,
    'RESET_VIEW': False
}


# default map projection
# Note: If set to EPSG:4326, then only EPSG:4326 basemaps will work.
DEFAULT_MAP_CRS = "EPSG:3857"

# Where should newly created maps be focused?
DEFAULT_MAP_CENTER = (0, 0)

# How tightly zoomed should newly created maps be?
# 0 = entire world;
# maximum zoom is between 12 and 15 (for Google Maps, coverage varies by area)
DEFAULT_MAP_ZOOM = 0

ALT_OSM_BASEMAPS = os.environ.get('ALT_OSM_BASEMAPS', False)
CARTODB_BASEMAPS = os.environ.get('CARTODB_BASEMAPS', False)
STAMEN_BASEMAPS = os.environ.get('STAMEN_BASEMAPS', False)
THUNDERFOREST_BASEMAPS = os.environ.get('THUNDERFOREST_BASEMAPS', False)
MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_ACCESS_TOKEN', '')
BING_API_KEY = os.environ.get('BING_API_KEY', None)
TIANDITU_API_KEY = os.environ.get('TIANDITU_API_KEY', None)

MAP_BASELAYERS += [
    {
        "source": {"ptype": "gxp_stamensource"},
        "name": "watercolor",
        "visibility": False,
        "group": "background",
        "title": "Stamen Watercolor"
    }, {
        "source": {"ptype": "gxp_stamensource"},
        "name": "toner",
        "visibility": False,
        "group": "background",
        "title": "Stamen Toner"
    },{
        "source": {
            "url": "http://services.arcgisonline.com/arcgis/rest/services/World_Shaded_Relief/MapServer",
            "ptype": "gxp_arcgiscachesource"},
        "group": "background",
        "name": "World Shaded Relief",
        "visibility": False,
        "fixed": True,
        "format": "jpeg",
        "tiled" : False,
        "title": "ESRI World Shaded Relief"
    },{
        "source": {
            "url": "http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer",
            "ptype": "gxp_arcgiscachesource"},
        "group": "background",
        "name": "World Street Map",
        "visibility": False,
        "fixed": True,
        "format": "jpeg",
        "tiled" : False,
        "title": "ESRI World Street Map"
    },{
      "source": {
          "url": "http://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer",
          "ptype": "gxp_arcgiscachesource"},
      "group": "background",
      "format": "jpeg",
      "name": "World Imagery",
      "visibility": False,
      "fixed": True,
      "tiled" : False,
      "title": "ESRI World Imagery"
      }, {
        "source": {
            "url": "http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer",
            "ptype": "gxp_arcgiscachesource"},
        "group": "background",
        "name": "Light Gray Canvas Base",
        "visibility": False,
        "fixed": True,
        "format": "jpeg",
        "tiled" : False,
        "title": "ESRI Light Gray Reference"
    },
    {
        "source": {
            "url": "http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer",
            "ptype": "gxp_arcgiscachesource"},
        "group": "background",
        "name": "Dark Gray Canvas Base",
        "visibility": False,
        "fixed": True,
        "format": "jpeg",
        "tiled" : False,
        "title": "ESRI Dark Gray Reference"
    },
    {
        "source": {
            "url": "http://gis.sinica.edu.tw/ccts/wmts",
            "ptype": "gxp_wmtssource",
            "title": "二十五萬分一中國圖(AMS L500)",
            },
        "group": "background",
        "name": "AMS_L500",
        "visibility": False,
        "fixed": True,
    }
]

if TIANDITU_API_KEY:
    MAP_BASELAYERS += [{
        "source": {
            "ptype": "gxp_tianditusource",
            "key":TIANDITU_API_KEY
        },
        "group": "background",
        "name": "TIANDITUROAD",
        "visibility": True,
        "fixed": True,
    }, {
        "source": {
            "ptype": "gxp_tianditusource",
            "key":TIANDITU_API_KEY
        },
        "group": "background",
        "name": "TIANDITUIMAGE",
        "visibility": False,
        "fixed": True,
    }, {
        "source": {
            "ptype": "gxp_tianditusource",
            "key":TIANDITU_API_KEY
        },
        "group": "background",
        "name": "TIANDITUTERRAIN",
        "visibility": False,
        "fixed": True,
    }, {
        "source": {
            "ptype": "gxp_tianditusource",
            "key":TIANDITU_API_KEY
        },
        "group": "background",
        "name": "TIANDITUANNOTATION",
        "visibility": True,
        "fixed": True,
    }]

baselayers = MAP_BASELAYERS
MAP_BASELAYERS = [LOCAL_GEOSERVER]
MAP_BASELAYERS.extend(baselayers)

# notification settings
NOTIFICATION_ENABLED = False

# notifications backends
_EMAIL_BACKEND = "pinax.notifications.backends.email.EmailBackend"
PINAX_NOTIFICATIONS_BACKENDS = [
    ("email", _EMAIL_BACKEND),
]

# Queue non-blocking notifications.
PINAX_NOTIFICATIONS_QUEUE_ALL = False
PINAX_NOTIFICATIONS_LOCK_WAIT_TIMEOUT = -1

# pinax.notifications
# or notification
NOTIFICATIONS_MODULE = 'pinax.notifications'

CORS_ORIGIN_ALLOW_ALL = True

MONITORING_ENABLED = False
# add following lines to your local settings to enable monitoring
if MONITORING_ENABLED:
    INSTALLED_APPS += ('geonode.contrib.monitoring',)
    MIDDLEWARE_CLASSES += ('geonode.contrib.monitoring.middleware.MonitoringMiddleware',)
    MONITORING_CONFIG = None
    MONITORING_HOST_NAME = 'localhost'
    MONITORING_SERVICE_NAME = 'local-geonode'
    MONITORING_HOST_NAME = SITE_HOST_NAME

GEOIP_PATH = os.path.join(os.path.dirname(__file__), '..', 'GeoLiteCity.dat')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s'
        },
        'simple': {
            'format': '%(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'INFO',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'INFO', 'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"], "level": "INFO", },
        "geonode": {
            "handlers": ["console"], "level": "INFO", },
        "gsconfig.catalog": {
            "handlers": ["console"], "level": "INFO", },
        "owslib": {
            "handlers": ["console"], "level": "INFO", },
        "pycsw": {
            "handlers": ["console"], "level": "INFO", },
        "camp": {
            "handlers": ["console"], "level": "DEBUG", },
        },
    }

############################################
# other settings specific to WorldMap CAMP #
############################################

# per-deployment settings should go here
SITE_HOST_NAME = os.getenv('SITE_HOST_NAME', "localhost")
SITE_HOST_PORT = os.getenv('SITE_HOST_PORT', "8000")

# use the WorldMap client
GEONODE_CLIENT_HOOKSET = 'geonode_worldmap.hooksets.WorldMapHookSet'
CORS_ORIGIN_WHITELIST = (
    HOSTNAME
)

#Define email service on GeoNode
EMAIL_ENABLE = True

if EMAIL_ENABLE:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST', default='')
    EMAIL_PORT = 25
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', default='')
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

PG_WORLDMAP_DJANGO_DB = os.getenv('PG_WORLDMAP_DJANGO_DB', "worldmap")
PG_WORLDMAP_UPLOADS_DB = os.getenv('PG_WORLDMAP_UPLOADS_DB', "wmdata")

DATABASES = {
    'default': {
         'ENGINE': 'django.contrib.gis.db.backends.postgis',
         'NAME': 'worldmap',
         'USER': 'worldmap',
         'PASSWORD': 'worldmap',
         'HOST' : 'localhost',
         'PORT' : '5432',
         'CONN_TOUT': 900,
     },
    # vector datastore for uploads
    'wmdata' : {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'wmdata',
        'USER' : 'worldmap',
        'PASSWORD' : 'worldmap',
        'HOST' : 'localhost',
        'PORT' : '5432',
        'CONN_TOUT': 900,
    }
}

OGC_SERVER['default']['DATASTORE']= os.getenv('DEFAULT_BACKEND_DATASTORE', 'wmdata')

# If you want to enable Mosaics use the following configuration
UPLOADER = {
    # 'BACKEND': 'geonode.rest',
    'BACKEND': 'geonode.importer',
    'OPTIONS': {
        'TIME_ENABLED': True,
        'MOSAIC_ENABLED': False,
        'GEOGIG_ENABLED': False,
    },
    'SUPPORTED_CRS': [
        'EPSG:4326',
        'EPSG:3785',
        'EPSG:3857',
        'EPSG:900913',
        'EPSG:32647',
        'EPSG:32736'
    ]
}


### WorldMap Settings ###


# for now we remove CsrfViewMiddleware, which creates failures on x-csrftoken
# We need to fix this

# MIDDLEWARE_CLASSES += (
#     # 'django.middleware.csrf.CsrfViewMiddleware', # remove csrf because it will stop users from extranet
#     # Add cache middleware for the per-site cache
#     'django.middleware.cache.UpdateCacheMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.cache.FetchFromCacheMiddleware',
# )

# Other settings
USE_CUSTOM_ORG_AUTHORIZATION = True
# Modify affiliate defaults
CUSTOM_ORG_AUTH_TEXT = _("Are you affiliated with Zhejiang University?")
# Modify the link of terms and condition
CUSTOM_AGREE_TOS_TEXT = _("I agree to the <a href='/aboutus/#disclaimer'>Terms and Conditions</a>")
# Uncomment following line if debugging GeoExplorer static files
# GEONODE_CLIENT_LOCATION = 'http://localhost:9090/'

# Set TIME_ZONE to Shanghai and close USE_TZ to change the time showed in browser
USE_TZ = True
# Modify language settings
LANGUAGE_CODE = 'zh-cn'
MODELTRANSLATION_LANGUAGES = [LANGUAGE_CODE, ]
MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGE_CODE
MODELTRANSLATION_FALLBACK_LANGUAGES = (LANGUAGE_CODE,)

# Modify the default permission of download data from true to false
# DEFAULT_ANONYMOUS_VIEW_PERMISSION = strtobool(
#     os.getenv('DEFAULT_ANONYMOUS_VIEW_PERMISSION', 'True')
# )
# DEFAULT_ANONYMOUS_DOWNLOAD_PERMISSION = strtobool(
#     os.getenv('DEFAULT_ANONYMOUS_DOWNLOAD_PERMISSION', 'False')
# )

# Add share links
SOCIAL_ORIGINS += [{
    "label": _("WeChat Moments"),
    "url": "http://api.addthis.com/oexchange/0.8/forward/wechat/offer?url={url}&title={name}",
    "css_class": "wx"
}, {
    "label": _("QQ"),
    "url": "http://connect.qq.com/widget/shareqq/index.html?url={url}&title={name}&summary={abstract}",
    "css_class": "qq"
}, {
    "label": _("Qzone"),
    "url": "http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url={url}&title={name}&summary={abstract}",
    "css_class": "qz"
}, {
    "label": _("Tencent Microblog"),
    "url": "http://share.v.t.qq.com/index.php?c=share&a=index&title={name}&url={url}&line1={abstract}",
    "css_class": "tm"
}, {
    "label": _("Sina Microblog"),
    "url": "http://service.weibo.com/share/share.php?title={name}&url={url}",
    "css_class": "sm"
}, {
    "label": _("Renren Inc"),
    "url": "http://widget.renren.com/dialog/share?resourceUrl={url}&title={name}&description={abstract}",
    "css_class": "rri"
}, {
    "label": _("Baidu Post Bar"),
    "url": "http://tieba.baidu.com/f/commit/share/openShareApi?url={url}&title={name}",
    "css_class": "bpb"
}, {
    "label": _("Douban"),
    "url": "http://shuo.douban.com/!service/share?href={url}&name={name}&text={abstract}",
    "css_class": "db"
}]

# Remove google earth from download formats
DOWNLOAD_FORMATS_VECTOR = [
    'JPEG', 'PDF', 'PNG', 'Zipped Shapefile', 'GML 2.0', 'GML 3.1.1', 'CSV',
    'Excel', 'GeoJSON', 'KML', 'Tiles',
    'QGIS layer file (.qlr)',
    'QGIS project file (.qgs)',
]
DOWNLOAD_FORMATS_RASTER = [
    'JPEG',
    'PDF',
    'PNG',
    'ArcGrid',
    'GeoTIFF',
    'Gtopo30',
    'ImageMosaic',
    'KML',
    # 'View in Google Earth',
    'Tiles',
    'GML',
    'GZIP',
    'QGIS layer file (.qlr)',
    'QGIS project file (.qgs)',
    'Zipped All Files'
]
# Modify the copyright in mapview
WM_COPYRIGHT_URL = os.getenv('WM_COPYRIGHT_URL', "http://www.zju.edu.cn/")
WM_COPYRIGHT_TEXT = os.getenv('WM_COPYRIGHT_TEXT', _("Bigdata and AMAP Innovation Team"))

#ALLOWED_HOSTS = ['localhost', '127.0.0.1', '10.202.70.121', '::1']
# PROXY_ALLOWED_HOSTS = ('localhost', '127.0.0.1', '10.202.70.121', '::1', 'amap.zju.edu.cn', )
# Add required settings for cache
# CACHE_MIDDLEWARE_ALIAS # The cache alias to use for storage.
CACHE_MIDDLEWARE_SECONDS = 15 # The number of seconds each page should be cached.
CACHE_MIDDLEWARE_KEY_PREFIX = 'Camp' # 如果缓存被多个使用相同Django安装的网站所共享，那么把这个值设成当前网站名，或其他能代表这个Django实例的唯一字符串，以避免key发生冲突。如果你不在意的话可以设成空字符串。
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',  # 指定缓存使用的引擎
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT':15,# default:300, None: never timeout
    }
}

DEFAULT_MAP_ABSTRACT = _("<h4>About Us</h4><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A large amount of geographical information which is closely related to human activities exists in the brilliant human civilization, numerous documents since ancient times, as well as the vast land and ocean. For example, the geographical distribution of individuals, the traces and the social relations for a single person, the migration of a group, as well as the existence, distribution and change of a region and trajectory for non-living things; as for a place, it also contains the people, events, things and other geographical information in previous time.</p><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The Academic Map Publishing Platform, established by Zhejiang University and Harvard University together, is not only an integrated database providing multi-functional query services, but also a display platform ready for users to present their research productions about geographic information and visualize analysis and select. The big data formed by the platform, will greatly contribute to future scientific research, overnment decision-making and social services.</p>")

CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',
    'http://localhost:8080',
]
