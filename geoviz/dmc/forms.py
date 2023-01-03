from django.forms import ModelForm
from bootstrap_daterangepicker import widgets, fields
from .models import *
from leaflet.forms.widgets import LeafletWidget
from django.forms.widgets import CheckboxSelectMultiple
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






