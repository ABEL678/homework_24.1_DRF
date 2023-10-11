from rest_framework.serializers import ValidationError
import re


class LinksValidator:

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        for field in self.fields:
            text = value.get(field, '')
            if self.has_external_links(text):
                raise ValidationError('Forbidden link')

    def has_external_links(self, text):
        links = re.findall(r'(?:https?://|www\.)?([^\s./?#]+)(?:\.[^\s./?#]+)', text)
        for link in links:
            if 'youtube.com' not in link:
                return True
        return False
