from django.forms import ModelForm 
from django import forms

from bootstrap_daterangepicker import widgets, fields
from .models import *
from leaflet.forms.widgets import LeafletWidget
from django.forms.widgets import CheckboxSelectMultiple

import requests, json
from crispy_forms.layout import Layout, Div, Field, Submit
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper

class dmcForm(ModelForm):
    datetime_range =fields.DateTimeRangeField(
        input_formats=['%d/%m/%Y (%H:%M)'],
        widget=widgets.DateTimeRangeWidget(format='%d/%m/%Y (%H:%M)',
                                           picker_options={
                                               'timePicker24Hour':True,

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

    drone_type= forms.ChoiceField(
        widget=forms.RadioSelect(), 
        choices=(('1', 'Drone'), ('2', 'Otter')),label="Drone project type",
        
        )
    
    mision_name = forms.MultipleChoiceField( 
        widget=forms.SelectMultiple(attrs={'size':20}),
        
        label="Select name of flight mission",
        choices=()
        )
    datetime_range = forms.CharField( label='datetime range') 

    takeoff_landing_coordinates=MultiPointField(srid=4326,help_text='Placename and GPS coordinates/Marks on map', null=True, blank=True,
                             verbose_name="Take-off and landing co-ordinates")
    flight_altitude = forms.IntegerField( label='Flight Altitude (meter)')
                                          
    image_overlap = forms.IntegerField(  label='Image Overlap')

    cloud_cover = forms.IntegerField(label='Cloud cover estimated at the Start of the flight in percentage')
    wind_speed =forms.IntegerField(  label='Wind Speed (meter/second)')
    wind_direction  = forms.CharField(label='Wind Direction ')
    air_temperature =forms.IntegerField(label='Air Temperatur (<sup> o</sup>C)')
    cdom =forms.IntegerField(label='Cdom– ug/l Quinine sulphate (0-500 -upper figure is a maximum guess and should be adjustable)')
    turbidity =forms.IntegerField(label='Turbidity- FNU (0-100)')
    Salinity =forms.IntegerField(label='Salinity- PSU (0-40)')
    water_temperature =forms.IntegerField(label='Water Temperature (1.7<sup> o</sup>C – 35<sup> o</sup>C)')
    secchi_depth=forms.IntegerField(label='Secchi Depth (metres)')

        
    dron_info_manufacturer = forms.CharField(label="Manufacturer")
    dron_info_drone_srnr= forms.CharField( label="Serial number")
    dron_info_make= forms.CharField( label="Make")
    dron_info_model= forms.CharField( label="Model")
    dron_info_type= forms.CharField( label='Type')
    dron_info_year =forms.IntegerField(label='Year')
    
    
     
    sensor_info_make = forms.CharField( label="Make")
    sensor_info_model = forms.CharField( label="Model")
    sensor_info_type = forms.CharField( label='Type')
    sensor_info_sensor_size =forms.CharField( label='Sensor size')
    sensor_info_resolution = forms.CharField( label='Resolution')
    sensor_info_band_wavelength_intervals = forms.CharField( label='Band wavelength intervals')
    sensor_info_dates_last_calibration=forms.DateField( label='Dates of last calibration')
    sensor_info_dates_last_maintenance  = forms.DateField( label='Dates of last maintenance',
                                              )
    
    
    # All uploaded
    # #mosaiced_image = models.FileField(null=True, blank=True, verbose_name='Upload single mosaiced file', upload_to='dmcData/mosaiced/')
    
    # mosaiced_image = models.FileField(null=True, blank=True,
    #                                   storage=MinioBackend(bucket_name='dmc'),
    #                                   verbose_name='Upload single mosaiced file',
    #                                   upload_to=iso_date_prefix)
    # row_image = models.FileField(null=True, blank=True, verbose_name='Upload raw images a single .zip file', upload_to='dmcData/rowImages/')
    # ground_control_point = models.FileField(null=True, blank=True, verbose_name='Upload ground control point as .csv', upload_to='dmcData/ground_control_point/')
    # ground_truth_point = models.FileField(null=True, blank=True, verbose_name='Upload ground truth point as .csv', upload_to='dmcData/ground_truth_point/')
    # dronePath = models.FileField(null=True, blank=True, verbose_name='Upload drone path file as .kml',
    #                                       upload_to='dmcData/donePath')

    def __init__(self, *args, **kwargs):
            super(ddcForm, self).__init__(*args, **kwargs)
    
            obj = requests.get(f'http://localhost:8000/api/dronproject/').json()
            
            self.fields['mision_name'].choices = [(val['Identifier'], val['Flight Name']) for val in obj]
            
            
            
            self.helper = FormHelper()
            self.helper.layout = Layout(
            InlineRadios('drone_type'),
            )
            #self.helper.add_input(Submit('submit', 'Submit'))

