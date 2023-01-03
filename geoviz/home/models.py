from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
User= settings.AUTH_USER_MODEL

# Create your models here.


gender_category_choices = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("undisclosed ", "Undisclosed"),
)


organisation_choice = (
    ("Norwegian Institute for Water Research ", "Norwegian Institute for Water Research "),
    ("Norwegian University for Science and Technology", "Norwegian University for Science and Technology"),
    ("Norwegian Computing Center", "Norwegian Computing Center"),
    ("Grid-Arendal", "Grid-Arendal"),
    ("Norwegian Institute for Nature Research", "Norwegian Institute for Nature Research"),
    ("Institute for Marine Research", "Institute for Marine Research"),
    ("Spectrofly Aps", "Spectrofly Aps"),
    ("Andøya Space Center", "Andøya Space Center"),
    ("UNINETT/Sigma2", "UNINETT/Sigma2"),
    ("Weag Solutions AS", "Weag Solutions AS"),
    ("Miljødirektoratet", "Miljødirektoratet"),
    ("Uni of Southern Denmark", "Uni of Southern Denmark"),
    ("University of Exeter", "University of Exeter"),
    ("University of Tromsø", "University of Tromsø"),
    ("The Research Council of Norway", "The Research Council of Norway"),
    ("SeaBee", "SeaBee"),
    ("Other", "Other"),
)








class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    fist_name= models.CharField(max_length=300, null=False, blank=False,verbose_name="First name")
    last_name= models.CharField(max_length=300, null=False, blank=False,verbose_name="Last name")
    sex = models.CharField(choices=gender_category_choices, max_length=300,null=True,blank=True,verbose_name="Gender")
    organisation = models.CharField(choices=organisation_choice, max_length=300, null=False, blank=False, verbose_name="Organisation you represent? ")
    organisation_other = models.CharField(max_length=300, null=True, blank=True,verbose_name="Please specify your organisation")
    pesonal_profile = models.URLField(max_length=300, null=True, blank=True,verbose_name="Link to the personal profile page")
    agreement = models.BooleanField(null=False, blank=False, verbose_name="By clicking here, I state that I have read and understood the terms and conditions.")
    history = HistoricalRecords()


    def __str__(self):
        return str(self.user) or 'NA'


    class Meta:
        verbose_name_plural = "User profile"

