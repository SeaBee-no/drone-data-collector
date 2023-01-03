from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic.edit import CreateView ,UpdateView
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.shortcuts import redirect








# Create your views here.
#@login_required(login_url='/admin/login/')
def home(request):
    if request.user.is_authenticated and not hasattr(request.user, 'user_profile'):
        return redirect('profileAdd')
    else:
        return render(request, 'index.html')



#@login_required(login_url='/admin/login/')
def about(request):
    return render(request, 'about.html')

#@login_required(login_url='/admin/login/')
def team(request):
    return render(request, 'team.html')

#@login_required(login_url='/admin/login/')
def toolbox(request):
    return render(request, 'toolbox.html')

def geoviz(request):
    return render(request, 'geoviz.html')

#@login_required(login_url='/admin/login/')
def contact(request):
    return render(request, 'contact.html')

def disclaimer(request):
    return render(request, 'disclaimer.html')


class ProfileCreate(SuccessMessageMixin,CreateView):
    model = user_profile
    form_class = user_profilesForm
    template_name = "profile.html"
    success_message = "Your profile has been successfully created"
    #success_url = reverse_lazy('toolbox')
    def get_success_url(self):
        return reverse_lazy('profileUpdate', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        if (form.cleaned_data['organisation'] == 'Other' and form.cleaned_data['organisation_other'] is None ):
            form.add_error('organisation_other', 'Field required')
            return super(ProfileCreate, self).form_invalid(form)
        return super(ProfileCreate, self).form_valid(form)


class ProfileUpdate(SuccessMessageMixin,UpdateView):
    model = user_profile
    form_class = user_profilesForm
    success_message = "Your profile has been successfully updated"
    template_name = "profile.html"
    #success_url = reverse_lazy('toolbox')
    def get_success_url(self):
        return reverse_lazy('profileUpdate', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        #form.instance.user = self.request.user
        if (form.cleaned_data['organisation'] == 'Other' and form.cleaned_data['organisation_other'] is None ):
            form.add_error('organisation_other', 'Field required')
            return super(ProfileUpdate, self).form_invalid(form)
        return super(ProfileUpdate, self).form_valid(form)





