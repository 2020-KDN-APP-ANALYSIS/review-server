from django.http import JsonResponse
from .parser import PlaystoreAppParser
# Create your views here.
def icon_view(request,app_id):
    if request.method == "GET":
        url = 'https://play.google.com/store/apps/details?id=' + app_id + '&hl=ko&gl=KR'
        playstore_app_parser = PlaystoreAppParser(url)
        icon_url = playstore_app_parser.get_icon()
        return JsonResponse({'icon' : icon_url})

def title_view(request, app_id):
    if request.method == "GET":
        url = 'https://play.google.com/store/apps/details?id=' + app_id + '&hl=ko&gl=KR'
        playstore_app_parser = PlaystoreAppParser(url)
        title_url = playstore_app_parser.get_title()
        return JsonResponse({'title' : title_url})
    
def publisher_view(request, app_id):
    if request.method == "GET":
        url = 'https://play.google.com/store/apps/details?id=' + app_id + '&hl=ko&gl=KR'
        playstore_app_parser = PlaystoreAppParser(url)
        publisher_url = playstore_app_parser.get_publisher()
        return JsonResponse({'publisher' : publisher_url})
    
def description_view(request, app_id):
    if request.method == "GET":
        url = 'https://play.google.com/store/apps/details?id=' + app_id + '&hl=ko&gl=KR'
        playstore_app_parser = PlaystoreAppParser(url)
        description_url = playstore_app_parser.get_description()
        return JsonResponse({'description' : description_url})
    
def matrials_view(request, app_id):
    if request.method == "GET":
        url = 'https://play.google.com/store/apps/details?id=' + app_id + '&hl=ko&gl=KR'
        playstore_app_parser = PlaystoreAppParser(url)
        matrials_url = playstore_app_parser.get_matrials()
        return JsonResponse({'matrials' : matrials_url})
    
def app_total_view(request, app_id):
    if request.method == "GET":
        url = 'https://play.google.com/store/apps/details?id=' + app_id + '&hl=ko&gl=KR'

        playstore_app_parser = PlaystoreAppParser(url)

        total_url = {}

        total_url['icon'] = playstore_app_parser.get_icon()
        total_url['title'] =  playstore_app_parser.get_title()
        total_url['publisher'] = playstore_app_parser.get_publisher()
        total_url['description'] = playstore_app_parser.get_description()

        matrials = playstore_app_parser.get_matrials()
        total_url['video'] = matrials[0]
        total_url['image'] = matrials[1]
        
        return JsonResponse(total_url)