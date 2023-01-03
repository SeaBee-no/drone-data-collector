from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.sites.shortcuts import get_current_site




expertise_in_plastic_pollution_choice = (
("macro", "MACRO"),
("micro", "	MICRO"),
("nano", "NANO"),
("biology", "Biology"),
("chemistry", "Chemistry"),
("physics", "Physics"),
("risk assessment", "Risk assessment"),
("geochemistry", "Geochemistry"),
("modelling", "Modelling"),
("other", "Other"),
)



# return full url in the modelform
def buildFullUrl(val):
    request = None
    full_url = ''.join(['http://', get_current_site(request).domain,'/', val])
    return full_url

class user_profilesForm(ModelForm):


    class Meta:
        model = user_profile
        fields = '__all__'
        exclude = ()
        labels = {
            "agreement": "<span class='text-primary' >By clicking here, I state that I have read and understood the <u> <a target='_blank' href= " + buildFullUrl(
                'disclaimer') + " >terms and conditions.</a></u></span>*",

        }
        widgets = {
            'agreement': forms.CheckboxInput(attrs={'style': 'width:15px;height:15px','required': 'False' }, ),

        }

