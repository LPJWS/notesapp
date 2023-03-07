from django.contrib import admin
from django.apps import apps
from .models import *
from django.utils.html import format_html

app = apps.get_app_config('notesapp')

for _, model in app.models.items():
    admin.site.register(model)
