from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from leaflet.admin import LeafletGeoAdmin
from .models import  *

# Register your models here.
class dmc_main_Admin(ImportExportModelAdmin,SimpleHistoryAdmin,LeafletGeoAdmin):
    #form = user_profilesForm
    list_display = ('mision_name',)
    search_fields = ('mision_name',)
admin.site.register(dmc_main,dmc_main_Admin )


class dmc_droneInfo_Admin(ImportExportModelAdmin,SimpleHistoryAdmin):
    #form = user_profilesForm
    list_display = ('model',)
    search_fields = ('model',)
admin.site.register(drone_info_list,dmc_droneInfo_Admin )

class dmc_sensorInfo_Admin(ImportExportModelAdmin,SimpleHistoryAdmin):
    #form = user_profilesForm
    list_display = ('model',)
    search_fields = ('model',)
admin.site.register(sensor_info_list,dmc_sensorInfo_Admin )
