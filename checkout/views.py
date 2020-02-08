from django.http import JsonResponse

from . import data
from .forms import OrderForm


def purchase_print(request):
    form = OrderForm(request.POST)
    if not form.is_valid():
        return JsonResponse(status=422, data=form.errors)
    details = data.process_order(form)
    return JsonResponse(status=201, data=details)
