# resources.py

from import_export import resources
from .models import DynamicURL

class DynamicURLResource(resources.ModelResource):
    class Meta:
        model = DynamicURL
        fields = ('path', 'title','meta_description')
