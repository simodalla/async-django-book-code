from django.conf import settings
from django.template.response import TemplateResponse


def locations(request):
    context = {
        "locations": settings.WEATHER_LOCATIONS,
    }
    return TemplateResponse(request, "djstorm-locations.html", context)


def locations2(request):
    context = {
        "locations": settings.WEATHER_LOCATIONS,
    }
    return TemplateResponse(request, "djstorm-locations2.html", context)
