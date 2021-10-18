from django.contrib import admin
from .models import Vacancy


class VacancyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Vacancy._meta.get_fields()]
    list_display_links = ('rpc', 'title')
    # list_editable = ()
    list_filter = ('rpc', 'title', 'url')


# Register your models here.
admin.site.register(Vacancy, VacancyAdmin)
