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
import os, base64
#from rest_framework import generics

from rest_framework.permissions import IsAuthenticated

from django.contrib import messages

from rest_framework import  generics

from django.views.decorators.csrf import csrf_exempt
from geo.Geoserver import Geoserver

from minio import Minio
from datetime import  timedelta
import urllib
jsonPath=Path.joinpath(conf_settings.BASE_DIR, 'dmc','tempfolder')


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
    other = serializers.FileField(required=False)
    
    
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




class get_download_url(generics.GenericAPIView):
        
        def get(self, request, fileWithPath ):
            try:
                minioClient = Minio(
                           "storage.seabee.sigma2.no",
                        access_key=os.getenv('MINIO_ACCESS_KEY'),
                        secret_key=os.getenv('MINIO_SECRET_KEY'),
                        )
                #found = minioClient.bucket_exists("dmc")
                fileWithPath = fileWithPath.replace("????", "/")
                file_url = minioClient.presigned_get_object("geoviz-upload-data", f"{fileWithPath}", expires=timedelta(hours=1))

                return Response(file_url)
                
            except Exception as e:
                print(e, flush=True)
                return Response('something wrong')






class publish_to_geonode(APIView):
    def get(self, request, format=None, filelocation=None ):
        try:

            http_request = request._request
            download_url_view = get_download_url.as_view()
            response = download_url_view(http_request, fileWithPath=filelocation)
            response_url = response.data
    
            file_name = Path(response_url.split("?")[0]).name
            file_stem = Path(response_url.split("?")[0]).stem
            file_extension = Path(response_url.split("?")[0]).suffix

            counter = 1
            while Path(jsonPath / file_name).exists():
                file_name = f"{file_stem}_{counter}.{file_extension}"
                counter += 1
            
            file_path_with_name = jsonPath / file_name

            urllib.request.urlretrieve(response_url, file_path_with_name)

            
            print(f"The file has been saved to:{file_path_with_name}")
            
            geo = Geoserver( 'https://geonode.seabee.sigma2.no/geoserver',   username=os.getenv('geoserver_user'),   password=os.getenv('geosever_pass'))
            geo.create_coveragestore(layer_name=file_stem, path=file_path_with_name, workspace='geonode')

            
            
            credentials = f"{os.getenv('geondoe_user')}:{os.getenv('geonode_pass')}".encode('utf-8')

            encoded_credentials = base64.b64encode(credentials).decode('utf-8')

            geonode_upload_tigger = "https://geonode.seabee.sigma2.no/api/v2/management/commands/"
            


            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Basic {encoded_credentials}"     
                            }
            # Define command and parameters
            command = "updatelayers"
            kwargs = {
            'filter': file_stem,
            'store': file_stem,
            'workspace':'geonode'
            }

            response = requests.post(geonode_upload_tigger, headers=headers, data=json.dumps({"command": command, "kwargs": kwargs}))
            
            job_id= response.json()['data']['id']

            #delete the temp file once uploded
            file_path_with_name.unlink()

            return Response({'jobid':job_id})


        except Exception as e:
            print(e, flush=True)
            return Response('something wrong')

class check_active_geonode_job(APIView):
        def get(self, request, format=None, jobid=None ):
            try:
                
                credentials = f"{os.getenv('geondoe_user')}:{os.getenv('geonode_pass')}".encode('utf-8')

                encoded_credentials = base64.b64encode(credentials).decode('utf-8')

                geonode_upload_tigger = f"https://geonode.seabee.sigma2.no/api/v2/management/jobs/{jobid}/status/"
                
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Basic {encoded_credentials}"
                    } 
                response = requests.get(geonode_upload_tigger, headers=headers)
                
                if(response.status_code != 200):
                    return Response({'status':'NA'})
                
                return Response({'status':response.json()['status']})

                     
                                    
            except Exception as e:
                print(e, flush=True)
                return Response('something wrong')