import json

from django.http import HttpResponse, JsonResponse

from . import data
from .forms import OrderForm


def purchase_print(request):
    if request.content_type != "application/json":
        return HttpResponse(status=415)
    form = OrderForm(json.loads(request.body))
    if not form.is_valid():
        return JsonResponse(status=422, data=form.errors)
    details = data.process_order(form)
    return JsonResponse(status=201, data=details)


def list_sizes(request):
    return HttpResponse(200)
