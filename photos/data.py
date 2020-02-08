from typing import Any, Dict

from .models import Catalog

DEFAULT_PAGE_SIZE = 20


def query_catalog(page_size, last_token) -> Dict[str, Any]:
    if not last_token and not page_size:
        photos = Catalog.objects.all()
    elif not last_token and page_size:
        photos = Catalog.objects.filter(id__lte=int(page_size))
    else:
        last_item = int(last_token) + (
            int(page_size) if page_size else DEFAULT_PAGE_SIZE
        )
        photos = Catalog.objects.filter(
            id__gt=int(last_token), id__lte=last_item
        )
    last_token = None if not photos else photos[len(photos) - 1].id
    return {
        "count": len(photos),
        "last_token": last_token,
        "results": [
            {
                "id": p.id,
                "title": p.title,
                "location": p.location,
                "year": p.year,
                "path": p.path,
            }
            for p in photos
        ],
    }
