from django.contrib import admin
from rango.models import Bares, Tapas
# Register your models here.

# Add in this class to customized the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Bares, CategoryAdmin)
admin.site.register(Tapas)
