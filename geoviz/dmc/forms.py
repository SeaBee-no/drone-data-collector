from django.forms import ModelForm
# from django import forms
from django.contrib.gis import forms

from bootstrap_daterangepicker import widgets, fields
from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import *
from leaflet.forms.widgets import LeafletWidget
from leaflet.forms.fields import GeometryCollectionField as MPF




from django.forms.widgets import CheckboxSelectMultiple

import requests
import json
from crispy_forms.layout import Layout, Div, Field, Submit
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper

from django.utils.safestring import mark_safe
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class dmcForm(ModelForm):
    datetime_range = fields.DateTimeRangeField(
        input_formats=['%d/%m/%Y (%H:%M)'],
        widget=widgets.DateTimeRangeWidget(format='%d/%m/%Y (%H:%M)',
                                           picker_options={
                                               'timePicker24Hour': True,

                                           }),

    )

    class Meta:
        model = dmc_main
        fields = '__all__'
        exclude = ()
        widgets = {
            'takeoff_landing_coordinates': LeafletWidget(),
        }

    def __init__(self, *args, **kwargs):

        super(dmcForm, self).__init__(*args, **kwargs)

        self.fields["dron_info"].widget = CheckboxSelectMultiple()
        self.fields["dron_info"].queryset = drone_info_list.objects.all()
        self.fields["sensor_info"].widget = CheckboxSelectMultiple()
        self.fields["sensor_info"].queryset = sensor_info_list.objects.all()


class ddcForm(forms.Form):
    created_by = forms.CharField(label="User")
    
    ## capture to db
    drone_type = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=(('Drone', 'Drone'), ('Otter', 'Otter'), ('Other', 'Other')), label="Drone Type", 
        required=True,
        disabled=True
    )

    flight_mission_guid = forms.CharField(
        label='flight GUID', disabled=False, required=False)

    mision_name_list = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(attrs={
            'size': 20,
            'style': 'width:100%;height:390px;'
        }),

        label="Select Name of Flight Mission",
        choices=(), required=False
    )
    mision_name = forms.CharField(
        label='Flight Mission Name', disabled=True, required=False
        # widget=forms.TextInput(attrs={'style':'width:60%'})
    )

    flight_datetime = forms.CharField(
        label='Flight Date Time', disabled=True, required=False)

    project_area_coordinates = MPF(
        srid=4326, geom_type='GEOMETRYCOLLECTION', required=False)

    project_location_coordinates = MPF(
        srid=4326, geom_type='GEOMETRYCOLLECTION', required=False)

    project_location_name = forms.CharField(
        label='Project Location', disabled=True, required=False)

    flight_duration = forms.CharField(
        label='Flight Duration in Minute', disabled=True, required=False)
    
    ## capture to db
    image_overlap = forms.IntegerField(label='Image Overlap', required=False,disabled=True)

    flight_altitude = forms.CharField(
        label='Flight AGL Altitude (meter)', disabled=True, required=False)

    cloud_cover = forms.CharField(
        label='Cloud Cover', required=False, disabled=True)

    humidity = forms.CharField(label='Humidity', disabled=True, required=False)

    air_temperature = forms.CharField(
        label='Air Temperatur', disabled=True, required=False)

    wind_speed = forms.CharField(
        label='Wind Speed', disabled=True, required=False)

    wind_direction = forms.CharField(
        label='Wind Direction', disabled=True, required=False)

    sun_time = forms.CharField(
        label='Day/Night', disabled=True, required=False)

    
    ## capture to db
    cdom = forms.IntegerField(
        label='Cdom– ug/l Quinine sulphate (0-500 -upper figure is a maximum guess and should be adjustable)', required=False, disabled=True)
   
     ## capture to db
    turbidity = forms.IntegerField(label='Turbidity- FNU (0-100)', required=False, disabled=True)
     
     ## capture to db
    salinity = forms.IntegerField(label='Salinity- PSU (0-40)', required=False, disabled=True)
    
     ## capture to db
    water_temperature = forms.IntegerField(
        label='Water Temperature (1.7<sup> o</sup>C – 35<sup> o</sup>C)', required=False, disabled=True)
    
     ## capture to db
    secchi_depth = forms.IntegerField(label='Secchi Depth (metres)', required=False, disabled=True)
    
    ## capture to db
    sensor_info_dates_last_calibration = forms.DateField(
        widget=DatePickerInput(
            options={
            "format": "MM/DD/YYYY",
            "showTodayButton": False,
        }
        ),
        label="Dates of last calibration",
        required=False,
       # disabled=True   
        )
     


     ## capture to db
    sensor_info_dates_last_maintenance = forms.DateField(
           widget=DatePickerInput(
            options={
            "format": "MM/DD/YYYY",
            "showTodayButton": False,
        },
           ),
          label='Dates of last maintenance', 
          required=False
            )
    
    mosaiced_image = forms.FileField(required=False, label='Upload your file1')
    mosaiced_image2 = forms.FileField(required=False, label='Upload your file2')


    
    def __init__(self, *args, **kwargs):
        super(ddcForm, self).__init__(*args, **kwargs)

        obj = requests.get(f'http://localhost:8000/api/dronproject/').json()


        self.fields['mision_name_list'].choices = [
            (val['Identifier'], val['Flight Name'] + "----" + val['Location']) for val in obj]

        self.helper = FormHelper()
        self.helper.layout = Layout(
        
            
        )

        # self.helper.add_input(Submit('submit', 'Submit'))