import csv
import json
import requests

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from geonode.base.models import TopicCategory, ResourceBase
from geonode.layers.models import Layer
from geonode.layers.views import layer_upload
from geonode.maps.models import Map

# get the major maps created by admin, or get the hotest and latest layer/map
def map_list_hottest(request):
    """
    return the six admin's/hottest/latest maps
    :param request: category[0:all the category 1-20: appointed category], type['hottest','latest']
    :return: json of resourcebase
    """
    resourcebase_dict = {}
    count = 0
    type = request.GET.get('type', '')
    # if type==admin key='owner_id' elseif type==hottest key=popular_count else type==latest key =date
    # order_by('-key'): the same with order by(key) asce

    if type == 'admin':
        key = 'owner_id'
    else:
        key = '-popular_count' if type == 'hottest' else '-date'

    if request.GET.get('category'):
        categoryid = int(request.GET.get('category'))
        resourcebase_queryset = ResourceBase.objects.instance_of(Map)\
        .filter(category_id=categoryid).order_by(key)[0:6]
    else:
        resourcebase_queryset = ResourceBase.objects.instance_of(Map)\
        .all().order_by(key,'-popular_count')[0:6]
    count = 0

    for resourcebase in resourcebase_queryset:
        thumb_url = resourcebase.thumbnail_url
        if hasattr(resourcebase, 'curatedthumbnail'):
            thumb_url = resourcebase.curatedthumbnail.img_thumbnail.url
        resourcebase_dict[count] = [resourcebase.title, resourcebase.owner.username\
        , thumb_url, resourcebase.detail_url\
        , resourcebase.popular_count\
        , resourcebase.date.strftime("%m-%d  %H:%M")]
        count = count + 1
    resourcebase_json = json.dumps(resourcebase_dict)
    return HttpResponse(resourcebase_json)


def selection_list(request):
    """
    This view returns a list of items added to the selection from the user in
    the current session in html or in csv.
    """
    if request.session.get('layer_ids'):
        layer_ids = request.session.get('layer_ids')
    else:
        layer_ids = []
    if request.session.get('map_ids'):
        map_ids = request.session.get('map_ids')
    else:
        map_ids = []
    layers = None
    maps = None

    if request.POST:
        if 'export_layers' in request.POST.dict() or 'export_maps' in request.POST.dict():
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="export.csv"'
            writer = csv.writer(response, dialect='excel')
            if 'export_layers' in request.POST.dict():
                resources = Layer.objects.filter(id__in=layer_ids).order_by('-title')
            if 'export_maps' in request.POST.dict():
                resources = Map.objects.filter(id__in=map_ids).order_by('-title')
            for res in resources:
                res_url = '%s%s' % (settings.SITEURL, res.get_absolute_url()[1:])
                writer.writerow(
                                [res.title.encode('utf-8'),
                                res.abstract.encode('utf-8'),
                                res_url])
            return response
        if 'clear' in request.POST.dict():
            request.session['layer_ids'] = None
            request.session['map_ids'] = None
    else:
        if 'item' in request.GET:
            res = ResourceBase.objects.get(id=int(request.GET['item']))
            if res.alternate:
                layer_ids.append(res.id)
            else:
                map_ids.append(res.id)
        else:
            url = request.META.get('HTTP_REFERER')
            if url:
                if '/layers/' in url or '/maps/' in url:
                    url = url.replace(settings.SITEURL, settings.SITEURL + 'api/')
                    req = requests.get(url)
                    object_ids = []
                    for obj in req.json()['objects']:
                        object_ids.append(obj['id'])
                    if '/layers/' in url:
                        layer_ids = list(set(layer_ids) | set(object_ids))
                    if '/maps/' in url:
                        map_ids = list(set(map_ids) | set(object_ids))

        request.session['layer_ids'] = layer_ids
        request.session['map_ids'] = map_ids
        layers = Layer.objects.filter(id__in=layer_ids).order_by('title')
        maps = Map.objects.filter(id__in=map_ids).order_by('title')

    return render(
        request,
        "selection/selection_list.html",
        { "layers": layers, "maps": maps, }
    )

@login_required
def layer_upload_wm(request, template='layers/layer_upload_standard.html'):
    print 'Using geonode.rest uploader'
    settings.UPLOADER['BACKEND'] = 'geonode.rest'
    return layer_upload(request, template)

@login_required
def layer_upload_geojson(request, template='layers/layer_upload_geojson.html'):
    print 'Using geonode.importer uploader'
    settings.UPLOADER['BACKEND'] = 'geonode.importer'
    return layer_upload(request, template)
