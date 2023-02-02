from django.contrib.auth.decorators import login_required
from django.http import  JsonResponse
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django.views.generic import CreateView, UpdateView , ListView, DeleteView

from rest_framework.views import APIView

from .forms import *
from .models import *
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework.response import Response


from rest_framework import serializers, status
from rest_framework import viewsets
from rest_framework import permissions

import requests, json, time
from django.shortcuts import render

from django.conf import settings as conf_settings
from pathlib import Path
import os
#from rest_framework import generics

from rest_framework.permissions import IsAuthenticated

from django.contrib import messages

from rest_framework import  generics

from django.views.decorators.csrf import csrf_exempt

#from rest_framework.permissions import IsAuthenticated 

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

jsonPath=Path.joinpath(conf_settings.BASE_DIR, 'dmc','dronelogbook')

class get_dronelogbook_flight_data_coustom_form (APIView):
    def get(self, request, format=None):
        try:
            
            # url = f'https://andoyaspace.dronelogbook.com/webservices/customReportAPI.php'
          
            # headers = {"accept": "application/json"}
            # data = {
            #     "apikey": os.environ['dronelogbooka_pikey'],
            #     "template": os.environ['dronelogbook_flight_template'],
            #     "page": "0",
            # }
            # obj= requests.post(url=url, data=data, headers= headers)

            # with open(jsonPath / 'flightList.json','w+') as json_file:
            #     json.dump(obj.json()['data'], json_file)

            with open(jsonPath / 'flightList.json','r') as f:
                obj = json.load(f)
            
            #return Response(obj.json()['data'])
            return Response(obj)

        except Exception as e:
            return Response('NA')



class get_flight_mission (APIView):
    
    #permission_classes = (IsAuthenticated,) 
    
    def get(self, request, format=None,opration=None,guid = None):
        try:
         
            obj= get_data_dlb_byguid(opration,guid)
            
            # with open(jsonPath / 'flight.json','w+') as json_file:
            #     json.dump(obj.json()['data'], json_file)

            return Response(obj.json()['data'])

        except Exception as e:
            return Response('NA')





def get_data_dlb_byguid(opration, guid):

        data = requests.get(f'https://api.dronelogbook.com/{opration}/{guid}', 
            headers={"accept": "application/json",
            "ApiKey": os.environ['dronelogbooka_pikey'],
             "DlbUrl": os.environ['dronelogbook_dlburl'],
            })
        # data = requests.get(f'https://api.dronelogbook.com/flight/DAE11F89-9DD6-D581-95B8-A4FF1FF1638E', 
        #     headers={
        #     "ApiKey": 'ak_f596ec84-c0d9-ea1e-46ab-77332e8fa36ehh',
        #     # "DlbUrl": 'www.dronelogbook.com',
        #     })

        return data

def get_data_dlb_bypage(opration,page_num):

        data = requests.get(f'https://api.dronelogbook.com/{opration}?num_page={page_num}', 
            headers={"accept": "application/json",
            "ApiKey": os.environ['dronelogbooka_pikey'],
             "DlbUrl": os.environ['dronelogbook_dlburl'],
            })

        return data


"""      flights = []
            has_more = 1
            data = []
            page_num = 0
            jsonPath=Path.joinpath(conf_settings.BASE_DIR, 'dmc','dronelogbook')
            while page_num != 4:
                page_num=page_num +1
                val  = get_data_dlb(page_num,'flight')
                flights = flights + val.json()['data']
                has_more = val.json()['has_more']
                print(page_num)
 """


       
@login_required(login_url='/admin/login/')
def ddc(request):
    context = {}
    form = ddcForm(request.POST or None)
    context['form'] = form
    return render(request, 'ddcEntryForm.html',context)




@login_required(login_url='/admin/login/')
def ddc_list(request):
    
    context = {}

    if request.user.is_superuser or request.user.is_staff:
        objList= ddc_main.objects.all().order_by('flight_mission_name')
    else:
        objList= ddc_main.objects.filter(created_by__user__username=request.user).order_by('flight_mission_name')

    context['objList'] = objList
    return render(request, 'ddcEntryList.html',context)




## to store addinonal parametr to database
class dronelogBook_serializers(serializers.ModelSerializer):
    class Meta:
        model = ddc_main
        fields = '__all__'
        #exclude = ('created_by',)

class dronelogBook_add(generics.CreateAPIView):

    #permission_classes = (IsAuthenticated,)
    queryset = ddc_main.objects.all()
    serializer_class = dronelogBook_serializers

    def perform_create(self, serializer):
        data = serializer.validated_data
        data["created_by"] = self.request.user
        serializer.save()
        return Response({"success": "Data has been successfully created."}, status=status.HTTP_201_CREATED)



class dronelogBook_update(generics.UpdateAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = ddc_main.objects.all()
    serializer_class = dronelogBook_serializers
    lookup_field = 'flight_mission_guid'

    def perform_update(self, serializer):
        data = serializer.validated_data
        data["created_by"] = self.request.user
        serializer.save()
        return Response({"success": "Data has been successfully updated."}, status=status.HTTP_200_OK)


class dronelogBook_recordcheck(generics.GenericAPIView):
    queryset = ddc_main.objects.all()
    serializer_class = dronelogBook_serializers

    def get(self, request, guid):
        instance = ddc_main.objects.filter(flight_mission_guid=guid)
        if not instance:
            return Response({"response": "not_found"}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance[0])
        return Response({"response": "found",'data':serializer.data}, status=status.HTTP_200_OK)



######################################################################################


## Upload data

class uploaddata_serializers(serializers.ModelSerializer):
    
    ## must be register the  filed in the serializers
    mosaiced_image = serializers.FileField(required=False)
    row_image = serializers.FileField(required=False)
    ground_control_point = serializers.FileField(required=False)
    ground_truth_point = serializers.FileField(required=False)
    dronePath = serializers.FileField(required=False)
    
    
    class Meta:
        model = ddc_upload
        fields = '__all__'



class uploaddata_add(generics.CreateAPIView):
    
    queryset = ddc_upload.objects.all()
    serializer_class = uploaddata_serializers

    def perform_create(self, serializer):
        try:
            serializer.save(**serializer.validated_data)
        except Exception as e:
            return Response({"error": "Failed to upload data. Error: {}".format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": "Data has been successfully uploded."}, status=status.HTTP_200_OK)



class uploaddata_update(generics.UpdateAPIView):
    
    queryset = ddc_upload.objects.all()
    serializer_class = uploaddata_serializers
    lookup_field = 'flight_mission_guid'

    def perform_update(self, serializer):
        try:
            serializer.save(**serializer.validated_data)
        except Exception as e:
            return Response({"error": "Failed to update data. Error: {}".format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": "Data has been successfully updated."}, status=status.HTTP_200_OK)


class uploaddata_delete(generics.DestroyAPIView):
    
    queryset = ddc_upload.objects.all()
    serializer_class = uploaddata_serializers
    lookup_field = 'flight_mission_guid'

    def perform_destroy(self, instance):
        file_field = self.request.data.get('field_to_delete', None)
        if file_field:
            file = getattr(instance, file_field, None)
            if file:
                try:
                    file.delete(save=True)
                    instance.save()
                    return Response({"success": "Field has been successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
                except Exception as e:
                    return Response({"error": f"Failed to delete field: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Field not specified."}, status=status.HTTP_400_BAD_REQUEST)



class uploadData_recordcheck(generics.GenericAPIView):
    queryset = ddc_upload.objects.all()
    serializer_class = uploaddata_serializers

    def get(self, request, guid):
        instance = ddc_upload.objects.filter(flight_mission_guid=guid)
        if not instance:
            return Response({"response": "not_found"}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance[0])
        return Response({"response": "found",'data':serializer.data}, status=status.HTTP_200_OK)


## to be tested 
def geonode_layer_update():
    try:
      
        geo = Geoserver( 'https://geonode.seabee.sigma2.no/geoserver',   username=user,   password=passw)
        geo.create_coveragestore(layer_name=file_path.name, path=file_path, workspace='geonode')
     
        
        credentials = "-----".encode('utf-8')

        encoded_credentials = base64.b64encode(credentials).decode('utf-8')

        url = "https://geonode.seabee.sigma2.no/api/v2/management/commands/"
        
        # headers = {
      
        #     "Authorization": f"Basic {encoded_credentials}"
        #     }
      
        # response = requests.get(url, headers=headers)
        # print(response.text)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}"     
                        }
        # Define command and parameters
        command = "updatelayers"
        kwargs = {
          'filter':'test_del.tif',
          'store':'test_del.tif',
          'workspace':'geonode'
        }

        response = requests.post(url, headers=headers, data=json.dumps({"command": command, "kwargs": kwargs}))

        # Check response
        if response.status_code == 201:
            print("Command successfully added.")
        else:
            print("Failed to add command.")
           
    
    except Exception as e:
        print (e)