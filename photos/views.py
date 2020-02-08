from django.http import JsonResponse
from django.views.decorators.http import require_GET

from . import data


@require_GET
def list_catalog(request):
    page_size = request.GET.get("page_size")
    last_token = request.GET.get("last_token")
    catalog = data.query_catalog(page_size, last_token)
    return JsonResponse(
        status=200, content_type="application/json", data=catalog,
    )
