from typing import Tuple
import requests
from html.parser import HTMLParser
from datetime import datetime
from django.utils import timezone

def preview_url(link) -> Tuple[datetime, str, str]:
    try:
        timestamp = timezone.now()
        url_instance = link.url
        req = requests.get(url_instance.raw_url)
        status_code = req.status_code
        content = req.content[:50]
        print(timestamp, status_code, content)
    except:
        pass
    title = 'PAGE-TITLE'
    return timestamp, title, status_code