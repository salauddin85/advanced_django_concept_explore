from django.contrib import admin
from django.apps import apps

app_models = apps.get_app_config('bulk_email').get_models()

for model in app_models:
    class DynamicAdmin(admin.ModelAdmin):
        list_display = [field.name for field in model._meta.fields]  
        
    try:
        admin.site.register(model, DynamicAdmin)
    except admin.sites.AlreadyRegistered:
        pass
