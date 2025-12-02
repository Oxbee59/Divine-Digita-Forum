# forum/templatetags/cloudinary_filters.py
from django import template
from urllib.parse import urlencode

register = template.Library()

@register.filter
def cloudinary_resize(file_url, size="w_900,h_500"):
    """
    Resize Cloudinary image/video URL safely.
    Example usage in template:
    {{ post.image.url|cloudinary_resize:"w_800,h_400" }}
    """
    if not file_url:
        return ""
    try:
        w, h = 900, 500
        if size:
            size_parts = size.split(",")
            for part in size_parts:
                if part.startswith("w_"):
                    w = int(part[2:])
                if part.startswith("h_"):
                    h = int(part[2:])
        params = urlencode({"f": "auto", "q": "auto", "w": w, "h": h, "c": "fill"})
        return f"{file_url}?{params}"
    except Exception:
        return file_url
