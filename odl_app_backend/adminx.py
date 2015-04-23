__author__ = 'chenghui'

# Register your models here.
import xadmin
from django.db.models import get_app, get_models

app = get_app('record')
for model in get_models(app):
    name = model._meta.verbose_name
    xadmin.site.register(model)