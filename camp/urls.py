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

from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.defaults import page_not_found

from tastypie.api import Api

from geonode.urls import urlpatterns

from .api import LayerResource, MapResource, OwnerResource, TopicCategoryResource
from .views import map_list_hottest, selection_list, layer_upload_geojson, layer_upload_wm

camp_api = Api(api_name='camp_api')
camp_api.register(LayerResource())
camp_api.register(MapResource())
camp_api.register(OwnerResource())
camp_api.register(TopicCategoryResource())

urlpatterns = [
    url(r'', include('geonode_worldmap.wm_extra.urls',
        namespace='worldmap')),
    url(r'', include('geonode_worldmap.gazetteer.urls',
        namespace='gazetteer')),
    url(r'', include('geonode_worldmap.mapnotes.urls',
        namespace='mapnotes'))
    ] + urlpatterns

urlpatterns = [
    # camp additional urls
    url(r'^/?$',
        TemplateView.as_view(template_name='site_index.html'),
        name='home'),
    url(r'^aboutus/$',
  	    TemplateView.as_view(template_name='aboutus.html'),
        name='aboutus'),
    url(r'^maps/list/hottest/$', map_list_hottest, name='map_list_hottest'),
    url(r'^selection/list/$', selection_list, name='selection_list'),
    # geojson upload (temp)
    url(r'^layers/upload$', layer_upload_wm, name='layer_upload_wm'),
    url(r'^layers/upload_geojson$', layer_upload_geojson, name='layer_upload_geojson'),
    # api
    url(r'^api/', include(camp_api.urls)),
    # urls to disable
    url('^services/', page_not_found, {'exception': Exception('Not Found')}),
] + urlpatterns
