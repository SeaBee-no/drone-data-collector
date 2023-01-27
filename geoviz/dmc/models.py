from django.contrib.gis.db.models.fields import MultiPointField
from django.conf import settings
User = settings.AUTH_USER_MODEL
from home.models import *
from django.contrib.postgres.fields import DateTimeRangeField
import datetime
from django_minio_backend import MinioBackend, iso_date_prefix

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.fields.files import FieldFile

windDirectionChoices= (
    ("N", "N"),
    ("NE", "NE"),
    ("E", "E"),
    ("SE", "SE"),
    ("S", "S"),
    ("SW", "SW"),
    ("W", "W"),
    ("NW", "NW"),
                 )
droneTypeChoices= (
    ("", ""),
    ("Fixed wing", "Fixed wing"),
    ("Roter", "Roter"),
)
sensorTypeChoices= (
    ("", ""),
    ("RGB", "RGB"),
    ("Multispectral", "Multispectral"),
)

def year_choices():
    return reversed([(r,r) for r in range(1900, datetime.date.today().year+1)])

class drone_info_list(models.Model):
    manufacturer = models.CharField(max_length=300, null=True, blank=True, verbose_name="Manufacturer")
    drone_srnr= models.CharField( max_length=300, null=True, blank=True, verbose_name="Serial number")
    make= models.CharField( max_length=300, null=True, blank=True, verbose_name="Make")
    model= models.CharField( max_length=300, null=True, blank=True, verbose_name="Model")
    type= models.CharField( max_length=300,  choices= droneTypeChoices, null=True, blank=True, verbose_name='Type')
    year =models.IntegerField(choices=year_choices(),null=True, blank=True, verbose_name='Year')
    history = HistoricalRecords()

    def __str__(self):
        return str(self.manufacturer) + '/' + str(self.make) +'/'+ str(self.drone_srnr) or 'NA'


    class Meta:
        verbose_name_plural = "Drone info"

class sensor_info_list(models.Model):

    make = models.CharField( max_length=300, null=True, blank=True, verbose_name="Make")
    model = models.CharField( max_length=300, null=True, blank=True, verbose_name="Model",unique=True)
    type = models.CharField( max_length=300, choices= sensorTypeChoices, null=True, blank=True, verbose_name='Type')
    sensor_size =models.CharField( max_length=300,null=True, blank=True, verbose_name='Sensor size')
    resolution = models.CharField( max_length=300,null=True, blank=True, verbose_name='Resolution')
    band_wavelength_intervals = models.CharField( max_length=300,null=True, blank=True, verbose_name='Band wavelength intervals')
    dates_last_calibration=models.DateField( verbose_name='Dates of last calibration', blank=True,null=True)
    dates_last_maintenance  = models.DateField( verbose_name='Dates of last maintenance',
                                              blank=True, null=True)


    history = HistoricalRecords()

    def __str__(self):
        return str(self.model) or 'NA'


    class Meta:
        verbose_name_plural = "Sensor Info"


class dmc_main(models.Model):
    created_by = models.ForeignKey(user_profile, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name='dmc_for_metadata')

    # DateTime Range Fields https://pypi.org/project/django-bootstrap-daterangepicker/

    mision_name = models.CharField( max_length=300, null=False, blank=False,
                                            verbose_name="Name of mission")
    datetime_range = DateTimeRangeField(verbose_name='datetime range',null=True,blank=True)


    takeoff_landing_coordinates=MultiPointField(srid=4326,help_text='Placename and GPS coordinates/Marks on map', null=True, blank=True,
                             verbose_name="Take-off and landing co-ordinates")
    flight_altitude = models.IntegerField(null=True, blank=True,
                                                     verbose_name='Flight Altitude (meter)')
    image_overlap = models.PositiveIntegerField(null=True, blank=True,
                                                     verbose_name='Image Overlap')

    cloud_cover = models.PositiveIntegerField(null=True, blank=True,
                                                     verbose_name='Cloud cover estimated at the Start of the flight in percentage')
    wind_speed =models.PositiveIntegerField(null=True, blank=True,
                                                     verbose_name='Wind Speed (meter/second)')
    wind_direction  = models.CharField(null=True, blank=True, max_length=300,
                                                          choices=windDirectionChoices,
                                                          verbose_name='Wind Direction ')
    air_temperature =models.PositiveIntegerField(null=True, blank=True,
                                                     verbose_name='Air Temperatur (<sup> o</sup>C)')
    cdom =models.PositiveIntegerField(null=True, blank=True,
                                                     verbose_name='Cdom– ug/l Quinine sulphate (0-500 -upper figure is a maximum guess and should be adjustable)')
    turbidity =models.PositiveIntegerField(null=True, blank=True,
                                                     verbose_name='Turbidity- FNU (0-100)')
    Salinity =models.PositiveIntegerField(null=True, blank=True,
                                                     verbose_name='Salinity- PSU (0-40)')
    water_temperature =models.PositiveIntegerField(null=True, blank=True,
                                                verbose_name='Water Temperature (1.7<sup> o</sup>C – 35<sup> o</sup>C)')
    secchi_depth=models.PositiveIntegerField(null=True, blank=True,
                                                verbose_name='Secchi Depth (metres)')

    dron_info = models.ManyToManyField(drone_info_list ,blank=True,  related_name='dmc_for_metadata', verbose_name='Drone Information')
    sensor_info = models.ManyToManyField(sensor_info_list,blank=True,  related_name='dmc_for_metadata',verbose_name='Sensor Information')
    # All uploaded
    mosaiced_image = models.FileField(null=True, blank=True, verbose_name='Upload single mosaiced file', upload_to='dmcData/mosaiced/')
    # mosaiced_image = models.FileField(null=True, blank=True,
    #                                   storage=MinioBackend(bucket_name='dmc'),
    #                                   verbose_name='Upload single mosaiced file',
    #                                   upload_to=iso_date_prefix)
    row_image = models.FileField(null=True, blank=True, verbose_name='Upload raw images a single .zip file', upload_to='dmcData/rowImages/')
    ground_control_point = models.FileField(null=True, blank=True, verbose_name='Upload ground control point as .csv', upload_to='dmcData/ground_control_point/')
    ground_truth_point = models.FileField(null=True, blank=True, verbose_name='Upload ground truth point as .csv', upload_to='dmcData/ground_truth_point/')
    dronePath = models.FileField(null=True, blank=True, verbose_name='Upload drone path file as .kml',
                                          upload_to='dmcData/donePath')

    history = HistoricalRecords()


    # ground_control_point
    # ground_truth_point

    def __str__(self):
        return str(self.mision_name) or 'NA'


    class Meta:
        verbose_name_plural = "Mission profile"



class ddc_main(models.Model):
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name='ddc_for_metadata')
    flight_mission_guid  = models.CharField(null=True, blank=True, max_length=300,verbose_name='Dronelogbook Id',unique=True)
    
    flight_mission_name  = models.CharField(null=True, blank=True, max_length=300,verbose_name='Flight Mission Name')
    
    drone_type  = models.CharField(null=False, blank=False, max_length=300,verbose_name='Drone Type')
    
    image_overlap  = models.PositiveIntegerField(null=True, blank=True, verbose_name='Image Overlap')

    cdom =models.PositiveIntegerField(null=True, blank=True,
                                                     verbose_name='Cdom– ug/l Quinine sulphate (0-500 -upper figure is a maximum guess and should be adjustable)')
    turbidity =models.PositiveIntegerField(null=True, blank=True,
                                                     verbose_name='Turbidity- FNU (0-100)')
    salinity =models.PositiveIntegerField(null=True, blank=True,
                                                     verbose_name='Salinity- PSU (0-40)')
    water_temperature =models.PositiveIntegerField(null=True, blank=True,
                                                verbose_name='Water Temperature (1.7C – 35C)')
    secchi_depth=models.PositiveIntegerField(null=True, blank=True,
                                                verbose_name='Secchi Depth (metres)')
    sensor_dates_last_calibration=models.DateField( verbose_name='Dates of last calibration', blank=True,null=True)
    sensor_dates_last_maintenance  = models.DateField( verbose_name='Dates of last maintenance',
                                              blank=True, null=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.flight_mission_name or 'NA'


    class Meta:
        verbose_name_plural = "Dronelogbook additional parameter"

def get_iso_date() -> str:
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    return f"{now.year}-{now.month}-{now.day}"

class ddc_upload(models.Model):
  
     

    def delete(self, *args, **kwargs):
        """
        Delete must be overridden because the inherited delete method does not call `self.file.delete()`.
        """
        self.mosaiced_image.delete()
        super(ddc_upload, self).delete(*args, **kwargs)


 

    flight_mission_guid  = models.CharField(null=True, blank=True, max_length=300,verbose_name='Dronelogbook Id',unique=True)

    mosaiced_image = models.FileField(verbose_name="Object Upload",
                                       storage=MinioBackend(  
                                           bucket_name='dmc', 
                                       ),
                                       upload_to=iso_date_prefix, null=False, blank=False)
    mosaiced_image2 = models.FileField(verbose_name="Object Upload",
                                       storage=MinioBackend(  
                                           bucket_name='dmc',
                                       ),
                                       upload_to=iso_date_prefix, null=False, blank=False)
    
     
    
    
    #  mosaiced_image = models.FileField(null=True, blank=True,
    #                                   storage=MinioBackend(bucket_name='dmc'),
    #                                   verbose_name='Upload single mosaiced file',
    #                                   upload_to=iso_date_prefix)
 
     
    history = HistoricalRecords()



    
    def __str__(self):
        return self.flight_mission_guid or 'NA'


    class Meta:
        verbose_name_plural = "Seabee bucket"