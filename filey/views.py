from django.http import JsonResponse


def ping(request):
    data = {"ping": 'Home Page because I am feeling fancy :)'}
    return JsonResponse(data)
