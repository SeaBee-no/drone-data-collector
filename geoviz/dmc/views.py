from django.contrib.auth.decorators import login_required
from django.http import  JsonResponse
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django.views.generic import CreateView, UpdateView , ListView, DeleteView
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from .forms import *
from .models import *
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework.response import Response


from rest_framework import serializers, status
from rest_framework import viewsets
from rest_framework import permissions

@method_decorator(login_required, name='dispatch')
class dmcCreate(SuccessMessageMixin, CreateView):
    model = dmc_main
    form_class = dmcForm
    template_name = "dmcEntryForm.html"
    success_message = "Your results has been successfully added"
    #success_url = reverse_lazy('dmcupdate')

    def get_success_url(self):
        return reverse_lazy('dmcupdate', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        response = super(dmcCreate, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        form.instance.created_by = self.request.user.user_profile
        response = super(dmcCreate, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
                'entryType': 'new',
            }
            return JsonResponse(data)
        else:
            return response




@method_decorator(login_required, name='dispatch')
class dmcUpdate(SuccessMessageMixin, UpdateView):
    model = dmc_main
    form_class = dmcForm
    template_name = "dmcEntryForm.html"
    success_message = "Your results has been successfully updated"
    #success_url = reverse_lazy('dmcupdate')

    def get_success_url(self):
        return reverse_lazy('dmcupdate', kwargs={'pk': str(self.object.pk)},)

    def form_invalid(self, form):

        response = super(dmcUpdate, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):

        # to be disable auto user add later if needed
        form.instance.created_by = self.request.user.user_profile

        response = super(dmcUpdate, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
                'entryType': 'update',
            }
            return JsonResponse(data)
        else:
            return response

    # def get_context_data(self, **kwargs):
    #     context = super(dmcUpdate, self).get_context_data(**kwargs)
    #     dmc_inputs = dmc_main.objects.values().filter(id=self.object.id)
    #     dmc_inputs = [entry for entry in dmc_inputs]
    #     context['doi_list'] = dmc_inputs[0]
    #     return context



@method_decorator(login_required, name='dispatch')
class DoiList(ListView):
    model = dmc_main
    #fields = ['created_by.user.username', ]
    template_name = "toolEntryFormList.html"


    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return dmc_main.objects.all().order_by('mision_name')
        else:
            return dmc_main.objects.filter(created_by__user__username=self.request.user).order_by('mision_name')



@method_decorator(login_required, name='dispatch')
class DoiDelete(DeleteView):
    model = dmc_main
    success_url = reverse_lazy('dmclist')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_queryset(self):
        if  self.request.user.is_superuser:
            return dmc_main.objects.all()
        else:
            return dmc_main.objects.filter(created_by__user__username=self.request.user)


class get_droneInfo(APIView):
    def get(self, request, format=None, type=None,qstr= None ):
        try:
            if type is not None and qstr is not None and type=='drone' :
                return Response(drone_info_list.objects.values().filter(drone_srnr=qstr)[0])
            elif type is not None and qstr is not None and type=='sensor' :
                return Response(sensor_info_list.objects.values().filter(model= qstr)[0])
            else:
                return Response('NA')

        except Exception as e:
            print(e, flush=True)
            return Response('something wrong')



class drone_info_list_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = drone_info_list
        fields = ['drone_srnr', 'make', 'model', 'type','year','manufacturer']

class sensor_info_list_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = sensor_info_list
        fields = ['make','model', 'type', 'sensor_size', 'resolution','band_wavelength_intervals','dates_last_calibration','dates_last_maintenance']




class drone_info_list_SnippetList(viewsets.ModelViewSet):

    queryset = drone_info_list.objects.all()
    serializer_class = drone_info_list_Serializer
    permission_classes = [permissions.IsAuthenticated]

    # def create(self, request):
    #     serializer = drone_info_list_Serializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class sensor_info_list_SnippetList(viewsets.ModelViewSet):

    queryset = sensor_info_list.objects.all()
    serializer_class = sensor_info_list_Serializer
    permission_classes = [permissions.IsAuthenticated]

    # def create(self, request):
    #     serializer = sensor_info_list_Serializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #
    # def retrieve(self, request, pk=None):
    #     return Response({'http_method': 'GET'})
    #
    # def update(self, request, pk=None):
    #     return Response({'http_method': 'PUT'})
    #
    # def partial_update(self, request, pk=None):
    #     return Response({'http_method': 'PATCH'})
    #
    # def destroy(self, request, pk=None):
    #     return Response({'http_method': 'DEL'})