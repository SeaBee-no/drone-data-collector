from django.urls import include,path
from .views import *
from rest_framework import routers

# define the router
router = routers.DefaultRouter()

# define the router path and viewset to be used
router.register(r'adddrone', drone_info_list_SnippetList,basename='adddrone')
router.register(r'addsensor', sensor_info_list_SnippetList,basename='addsensor')

urlpatterns = [
path('dmc',dmcCreate.as_view(), name='dmcadd'),
path('dmc/<int:pk>/', dmcUpdate.as_view(), name='dmcupdate'),
path('dmc/list', DoiList.as_view(), name='dmclist'),
path('dmc/<int:pk>/del', DoiDelete.as_view(), name='dmcdel',),
path('dmc/<str:type>/<str:qstr>/', get_droneInfo.as_view(), name='droneSensor'),
path(r'dmcapi/', include(router.urls)),
path('api-auth/', include('rest_framework.urls')),
path('api/dronproject/', get_dronelogbook_flight_data_coustom_form.as_view(), name='get_drone_data'),
path('api/flight/<str:opration>/<str:guid>/', get_flight_mission.as_view(), name='get_flight'),
path('ddc/', ddc, name='ddc'),

]