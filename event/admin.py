from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.apps import apps

app_models = apps.get_app_config('event').get_models()

for model in app_models:
    class DynamicAdmin(admin.ModelAdmin):
        list_display = [field.name for field in model._meta.fields]  
        search_fields = [field.name for field in model._meta.fields if field.__class__.__name__ == 'CharField']  # কেবল string ফিল্ডের জন্য সার্চ
        list_filter = [field.name for field in model._meta.fields if field.__class__.__name__ == 'BooleanField']
        ordering = [field.name for field in model._meta.fields if field.__class__.__name__ == 'DateTimeField']
        # prepopulated_fields = {"slug": ("name",)}
        
    try:
        admin.site.register(model, DynamicAdmin)
    except admin.sites.AlreadyRegistered:
        pass
