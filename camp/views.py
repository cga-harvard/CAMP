import json

from django.http import HttpResponse
from geonode.base.models import TopicCategory, ResourceBase
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
    if request.POST.has_key('type'):
        type = request.POST['type']
    # if type==admin key='owner_id' elseif type==hottest key=popular_count else type==latest key =date
    # order_by('-key'): the same with order by(key) asce
    if type == 'admin':
        key = 'owner_id'
    else:
        key = '-popular_count' if type == 'hottest' else '-date'
    if request.POST['category'] != '0':
        categoryid = int(request.POST['category'])
        resourcebase_queryset = ResourceBase.objects.instance_of(Map)\
        .filter(category_id=categoryid).order_by(key)[0:6]
    else:
        resourcebase_queryset = ResourceBase.objects.instance_of(Map)\
        .all().order_by(key,'-popular_count')[0:6]
    count = 0

    for resourcebase in resourcebase_queryset:
        resourcebase_dict[count] = [resourcebase.title, resourcebase.owner.username\
        , resourcebase.thumbnail_url, resourcebase.detail_url\
        , resourcebase.popular_count\
        , resourcebase.date.strftime("%m-%d  %H:%M")]
        count = count + 1
    resourcebase_json = json.dumps(resourcebase_dict)
    return HttpResponse(resourcebase_json)

