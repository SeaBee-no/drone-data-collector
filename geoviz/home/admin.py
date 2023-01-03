from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
from .models import  *

# Register your models here.


class user_profile_Admin(SimpleHistoryAdmin,ImportExportModelAdmin):
    #form = user_profilesForm
    list_display = ('fist_name', 'organisation')
    search_fields = ('fist_name', 'organisation')
admin.site.register(user_profile,user_profile_Admin )



