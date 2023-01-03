# Generated by Django 3.2 on 2023-01-03 07:50

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion
import django_minio_backend.models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='drone_info_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(blank=True, max_length=300, null=True, verbose_name='Manufacturer')),
                ('drone_srnr', models.CharField(blank=True, max_length=300, null=True, verbose_name='Serial number')),
                ('make', models.CharField(blank=True, max_length=300, null=True, verbose_name='Make')),
                ('model', models.CharField(blank=True, max_length=300, null=True, verbose_name='Model')),
                ('type', models.CharField(blank=True, choices=[('', ''), ('Fixed wing', 'Fixed wing'), ('Roter', 'Roter')], max_length=300, null=True, verbose_name='Type')),
                ('year', models.IntegerField(blank=True, choices=[(2023, 2023), (2022, 2022), (2021, 2021), (2020, 2020), (2019, 2019), (2018, 2018), (2017, 2017), (2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981), (1980, 1980), (1979, 1979), (1978, 1978), (1977, 1977), (1976, 1976), (1975, 1975), (1974, 1974), (1973, 1973), (1972, 1972), (1971, 1971), (1970, 1970), (1969, 1969), (1968, 1968), (1967, 1967), (1966, 1966), (1965, 1965), (1964, 1964), (1963, 1963), (1962, 1962), (1961, 1961), (1960, 1960), (1959, 1959), (1958, 1958), (1957, 1957), (1956, 1956), (1955, 1955), (1954, 1954), (1953, 1953), (1952, 1952), (1951, 1951), (1950, 1950), (1949, 1949), (1948, 1948), (1947, 1947), (1946, 1946), (1945, 1945), (1944, 1944), (1943, 1943), (1942, 1942), (1941, 1941), (1940, 1940), (1939, 1939), (1938, 1938), (1937, 1937), (1936, 1936), (1935, 1935), (1934, 1934), (1933, 1933), (1932, 1932), (1931, 1931), (1930, 1930), (1929, 1929), (1928, 1928), (1927, 1927), (1926, 1926), (1925, 1925), (1924, 1924), (1923, 1923), (1922, 1922), (1921, 1921), (1920, 1920), (1919, 1919), (1918, 1918), (1917, 1917), (1916, 1916), (1915, 1915), (1914, 1914), (1913, 1913), (1912, 1912), (1911, 1911), (1910, 1910), (1909, 1909), (1908, 1908), (1907, 1907), (1906, 1906), (1905, 1905), (1904, 1904), (1903, 1903), (1902, 1902), (1901, 1901), (1900, 1900)], null=True, verbose_name='Year')),
            ],
            options={
                'verbose_name_plural': 'Drone info',
            },
        ),
        migrations.CreateModel(
            name='sensor_info_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(blank=True, max_length=300, null=True, verbose_name='Make')),
                ('model', models.CharField(blank=True, max_length=300, null=True, unique=True, verbose_name='Model')),
                ('type', models.CharField(blank=True, choices=[('', ''), ('RGB', 'RGB'), ('Multispectral', 'Multispectral')], max_length=300, null=True, verbose_name='Type')),
                ('sensor_size', models.CharField(blank=True, max_length=300, null=True, verbose_name='Sensor size')),
                ('resolution', models.CharField(blank=True, max_length=300, null=True, verbose_name='Resolution')),
                ('band_wavelength_intervals', models.CharField(blank=True, max_length=300, null=True, verbose_name='Band wavelength intervals')),
                ('dates_last_calibration', models.DateField(blank=True, null=True, verbose_name='Dates of last calibration')),
                ('dates_last_maintenance', models.DateField(blank=True, null=True, verbose_name='Dates of last maintenance')),
            ],
            options={
                'verbose_name_plural': 'Sensor Info',
            },
        ),
        migrations.CreateModel(
            name='Historicalsensor_info_list',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('make', models.CharField(blank=True, max_length=300, null=True, verbose_name='Make')),
                ('model', models.CharField(blank=True, db_index=True, max_length=300, null=True, verbose_name='Model')),
                ('type', models.CharField(blank=True, choices=[('', ''), ('RGB', 'RGB'), ('Multispectral', 'Multispectral')], max_length=300, null=True, verbose_name='Type')),
                ('sensor_size', models.CharField(blank=True, max_length=300, null=True, verbose_name='Sensor size')),
                ('resolution', models.CharField(blank=True, max_length=300, null=True, verbose_name='Resolution')),
                ('band_wavelength_intervals', models.CharField(blank=True, max_length=300, null=True, verbose_name='Band wavelength intervals')),
                ('dates_last_calibration', models.DateField(blank=True, null=True, verbose_name='Dates of last calibration')),
                ('dates_last_maintenance', models.DateField(blank=True, null=True, verbose_name='Dates of last maintenance')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical sensor_info_list',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Historicaldrone_info_list',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('manufacturer', models.CharField(blank=True, max_length=300, null=True, verbose_name='Manufacturer')),
                ('drone_srnr', models.CharField(blank=True, max_length=300, null=True, verbose_name='Serial number')),
                ('make', models.CharField(blank=True, max_length=300, null=True, verbose_name='Make')),
                ('model', models.CharField(blank=True, max_length=300, null=True, verbose_name='Model')),
                ('type', models.CharField(blank=True, choices=[('', ''), ('Fixed wing', 'Fixed wing'), ('Roter', 'Roter')], max_length=300, null=True, verbose_name='Type')),
                ('year', models.IntegerField(blank=True, choices=[(2023, 2023), (2022, 2022), (2021, 2021), (2020, 2020), (2019, 2019), (2018, 2018), (2017, 2017), (2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981), (1980, 1980), (1979, 1979), (1978, 1978), (1977, 1977), (1976, 1976), (1975, 1975), (1974, 1974), (1973, 1973), (1972, 1972), (1971, 1971), (1970, 1970), (1969, 1969), (1968, 1968), (1967, 1967), (1966, 1966), (1965, 1965), (1964, 1964), (1963, 1963), (1962, 1962), (1961, 1961), (1960, 1960), (1959, 1959), (1958, 1958), (1957, 1957), (1956, 1956), (1955, 1955), (1954, 1954), (1953, 1953), (1952, 1952), (1951, 1951), (1950, 1950), (1949, 1949), (1948, 1948), (1947, 1947), (1946, 1946), (1945, 1945), (1944, 1944), (1943, 1943), (1942, 1942), (1941, 1941), (1940, 1940), (1939, 1939), (1938, 1938), (1937, 1937), (1936, 1936), (1935, 1935), (1934, 1934), (1933, 1933), (1932, 1932), (1931, 1931), (1930, 1930), (1929, 1929), (1928, 1928), (1927, 1927), (1926, 1926), (1925, 1925), (1924, 1924), (1923, 1923), (1922, 1922), (1921, 1921), (1920, 1920), (1919, 1919), (1918, 1918), (1917, 1917), (1916, 1916), (1915, 1915), (1914, 1914), (1913, 1913), (1912, 1912), (1911, 1911), (1910, 1910), (1909, 1909), (1908, 1908), (1907, 1907), (1906, 1906), (1905, 1905), (1904, 1904), (1903, 1903), (1902, 1902), (1901, 1901), (1900, 1900)], null=True, verbose_name='Year')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical drone_info_list',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Historicaldmc_main',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('mision_name', models.CharField(max_length=300, verbose_name='Name of mission')),
                ('datetime_range', django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, null=True, verbose_name='datetime range')),
                ('takeoff_landing_coordinates', django.contrib.gis.db.models.fields.MultiPointField(blank=True, help_text='Placename and GPS coordinates/Marks on map', null=True, srid=4326, verbose_name='Take-off and landing co-ordinates')),
                ('flight_altitude', models.IntegerField(blank=True, null=True, verbose_name='Flight Altitude (meter)')),
                ('image_overlap', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image Overlap')),
                ('cloud_cover', models.PositiveIntegerField(blank=True, null=True, verbose_name='Cloud cover estimated at the Start of the flight in percentage')),
                ('wind_speed', models.PositiveIntegerField(blank=True, null=True, verbose_name='Wind Speed (meter/second)')),
                ('wind_direction', models.CharField(blank=True, choices=[('N', 'N'), ('NE', 'NE'), ('E', 'E'), ('SE', 'SE'), ('S', 'S'), ('SW', 'SW'), ('W', 'W'), ('NW', 'NW')], max_length=300, null=True, verbose_name='Wind Direction ')),
                ('air_temperature', models.PositiveIntegerField(blank=True, null=True, verbose_name='Air Temperatur (<sup> o</sup>C)')),
                ('cdom', models.PositiveIntegerField(blank=True, null=True, verbose_name='Cdom– ug/l Quinine sulphate (0-500 -upper figure is a maximum guess and should be adjustable)')),
                ('turbidity', models.PositiveIntegerField(blank=True, null=True, verbose_name='Turbidity- FNU (0-100)')),
                ('Salinity', models.PositiveIntegerField(blank=True, null=True, verbose_name='Salinity- PSU (0-40)')),
                ('water_temperature', models.PositiveIntegerField(blank=True, null=True, verbose_name='Water Temperature (1.7<sup> o</sup>C – 35<sup> o</sup>C)')),
                ('secchi_depth', models.PositiveIntegerField(blank=True, null=True, verbose_name='Secchi Depth (metres)')),
                ('mosaiced_image', models.TextField(blank=True, max_length=100, null=True, verbose_name='Upload single mosaiced file')),
                ('row_image', models.TextField(blank=True, max_length=100, null=True, verbose_name='Upload raw images a single .zip file')),
                ('ground_control_point', models.TextField(blank=True, max_length=100, null=True, verbose_name='Upload ground control point as .csv')),
                ('ground_truth_point', models.TextField(blank=True, max_length=100, null=True, verbose_name='Upload ground truth point as .csv')),
                ('dronePath', models.TextField(blank=True, max_length=100, null=True, verbose_name='Upload drone path file as .kml')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='home.user_profile')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical dmc_main',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='dmc_main',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mision_name', models.CharField(max_length=300, verbose_name='Name of mission')),
                ('datetime_range', django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, null=True, verbose_name='datetime range')),
                ('takeoff_landing_coordinates', django.contrib.gis.db.models.fields.MultiPointField(blank=True, help_text='Placename and GPS coordinates/Marks on map', null=True, srid=4326, verbose_name='Take-off and landing co-ordinates')),
                ('flight_altitude', models.IntegerField(blank=True, null=True, verbose_name='Flight Altitude (meter)')),
                ('image_overlap', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image Overlap')),
                ('cloud_cover', models.PositiveIntegerField(blank=True, null=True, verbose_name='Cloud cover estimated at the Start of the flight in percentage')),
                ('wind_speed', models.PositiveIntegerField(blank=True, null=True, verbose_name='Wind Speed (meter/second)')),
                ('wind_direction', models.CharField(blank=True, choices=[('N', 'N'), ('NE', 'NE'), ('E', 'E'), ('SE', 'SE'), ('S', 'S'), ('SW', 'SW'), ('W', 'W'), ('NW', 'NW')], max_length=300, null=True, verbose_name='Wind Direction ')),
                ('air_temperature', models.PositiveIntegerField(blank=True, null=True, verbose_name='Air Temperatur (<sup> o</sup>C)')),
                ('cdom', models.PositiveIntegerField(blank=True, null=True, verbose_name='Cdom– ug/l Quinine sulphate (0-500 -upper figure is a maximum guess and should be adjustable)')),
                ('turbidity', models.PositiveIntegerField(blank=True, null=True, verbose_name='Turbidity- FNU (0-100)')),
                ('Salinity', models.PositiveIntegerField(blank=True, null=True, verbose_name='Salinity- PSU (0-40)')),
                ('water_temperature', models.PositiveIntegerField(blank=True, null=True, verbose_name='Water Temperature (1.7<sup> o</sup>C – 35<sup> o</sup>C)')),
                ('secchi_depth', models.PositiveIntegerField(blank=True, null=True, verbose_name='Secchi Depth (metres)')),
                ('mosaiced_image', models.FileField(blank=True, null=True, storage=django_minio_backend.models.MinioBackend(bucket_name='dmc'), upload_to=django_minio_backend.models.iso_date_prefix, verbose_name='Upload single mosaiced file')),
                ('row_image', models.FileField(blank=True, null=True, upload_to='dmcData/rowImages/', verbose_name='Upload raw images a single .zip file')),
                ('ground_control_point', models.FileField(blank=True, null=True, upload_to='dmcData/ground_control_point/', verbose_name='Upload ground control point as .csv')),
                ('ground_truth_point', models.FileField(blank=True, null=True, upload_to='dmcData/ground_truth_point/', verbose_name='Upload ground truth point as .csv')),
                ('dronePath', models.FileField(blank=True, null=True, upload_to='dmcData/donePath', verbose_name='Upload drone path file as .kml')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dmc_for_metadata', to='home.user_profile')),
                ('dron_info', models.ManyToManyField(blank=True, related_name='dmc_for_metadata', to='dmc.drone_info_list', verbose_name='Drone Information')),
                ('sensor_info', models.ManyToManyField(blank=True, related_name='dmc_for_metadata', to='dmc.sensor_info_list', verbose_name='Sensor Information')),
            ],
            options={
                'verbose_name_plural': 'Mission profile',
            },
        ),
    ]
