from typing import Tuple
import requests
from html.parser import HTMLParser
from datetime import datetime
from django.utils import timezone

def get_link_title(link) -> Tuple[datetime, str, str]:
    timestamp = timezone.now()
    try:
        url_instance = link.url
        req = requests.get(url_instance.raw_url)
        status_code = req.status_code
        content = req.content[:50]
        # print(timestamp, status_code, content)
        title = content
    except Exception as e:
        # status code 500 is ok. Throw exception on HTTP connection exception on our side.
        if not status_code:
            raise IOError(e) from e
        title = 'Error!'
    return timestamp, title, status_code