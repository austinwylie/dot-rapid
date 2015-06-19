from django.contrib import admin

# Register your models here.
from rapid.models import GeoView, Feature

admin.site.register(GeoView)
admin.site.register(Feature)