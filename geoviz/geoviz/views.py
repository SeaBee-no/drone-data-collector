from django.contrib import sitemaps
from django.urls import reverse
from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default.views import RegistrationView
from captcha.fields import ReCaptchaField


class UserProfileRegistrationForm(RegistrationFormUniqueEmail):
    fieldTest = ReCaptchaField()


class ExtraFieldRegistrationView(RegistrationView):
    form_class = UserProfileRegistrationForm


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'
    def items(self):
        return ['home','about','team','toolbox',]
    def location(self, item):
        return reverse(item)