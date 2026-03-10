import re
import bleach

from PIL import Image
from xml.etree import ElementTree as ET
from django.core.exceptions import ValidationError

ALLOWED_TAGS = ["a", "code", "i", "strong"]


def validate_username(username):

    if not re.fullmatch(r"[a-zA-Z0-9]+", username):
        raise ValidationError("Username must contain only latin letters and numbers")


def clean_comment_text(text):

    return bleach.clean(
        text, tags=ALLOWED_TAGS, attributes={"a": ["href", "title"]}, strip=True
    )


def validate_text_file(file):

    if not file.name.lower().endswith(".txt"):
        raise ValidationError("Only TXT files allowed")

    if file.size > 100 * 1024:
        raise ValidationError("Text file too large")




def validate_image(image):

    with Image.open(image) as img:
        if img.format not in ["JPEG", "PNG", "GIF"]:
            raise ValidationError(
                "Only JPG, PNG, GIF images are allowed"
            )


def validate_xhtml(text):
    try:
        ET.fromstring(f"<root>{text}</root>")
    except ET.ParseError:
        raise ValidationError(
            "HTML must be valid XHTML with properly closed tags"
        )
