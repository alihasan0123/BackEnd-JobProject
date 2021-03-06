from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .Serializers import *
from rest_framework import status
import datetime
import xml.etree.ElementTree as ET
# Create your views here.


class getId(APIView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        try:
            company_id = Company.objects.get(id=id)
            data = CompanySerializer(company_id, many=False)
            return Response({'company': data.data})

        except:
            message = {'detail': 'Company by Id don\'t exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class getName(APIView):
    def get(self, request, *args, **kwargs):
        Name = self.kwargs.get('Name')
        try:
            company_id = Company.objects.get(Name=Name)
            data = CompanySerializer(company_id, many=False)
            return Response({'company': data.data})

        except:
            message = {'detail': 'Company by this Name don\'t exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class getAll(APIView):
    def get(self, request):
        data = Company.objects.all()
        dataall = CompanySerializer(data, many=True)
        return Response(dataall.data)


class addNewCompany(APIView):
    def post(self, request):
        data = request.data
        try:
            company = Company(
                Name=data['Name'],
                Location=data['Location'],
                WebSite=data['WebSite'],
                About=data['About'],
                logo=data['logo'],
                TeamSize=data['team'],
                Categories=data['cat'],
            )
            company.save()
            company = CompanySerializer(company, many=False)
            return Response({'savedData': company.data})
        except:
            message = {'detail': 'Company by this Name Already Exists!!'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class getAllCategories(APIView):
    def get(self, request):
        categories = Job.objects.all().values('Classification')
        if categories is not None:
            l = []
            for i in categories:
                l.append(i['Classification'])
            list = set(l)
            cat = {}
            for i in list:
                cat[i] = l.count(i)
            return Response({'data': cat})
        return Response({'data': None})


class getAllCountries(APIView):
    def get(self, request):
        countries = Job.objects.all().values('Country')
        if countries is not None:
            l = []
            for i in countries:
                l.append(i['Country'])
            list = set(l)
            cat = {}
            for i in list:
                cat[i] = l.count(i)
            return Response({'data': cat})
        return Response({'data': None})


class getAllCompanies(APIView):
    def get(self, request):
        company = Job.objects.all().values('AdvertiserName', 'LogoURL')
        if company is not None:
            # print(company)
            l = []
            for i in company:
                l.append((i['AdvertiserName'], i['LogoURL']))
            list = set(l)
            for i in list:
                print(i)
            cat = {}
            for i in list:
                cat[i[0]] = [l.count(i), i[1]]
            print(cat)
            return Response({'data': cat})
        return Response({'data': None})


class getjobCountry(APIView):
    def get(self, request, *args, **kwargs):
        Name = self.kwargs.get('Country')
        jobs = None
        jobs = Job.objects.filter(Country=Name)
        jobs = JobSerializer(jobs, many=True)
        return Response({'Jobs': jobs.data})


class getJobsName(APIView):
    def get(self, request, *args, **kwargs):
        Name = self.kwargs.get('JobName')
        jobs = Job.objects.filter(AdvertiserName=Name)
        jobs = JobSerializer(jobs, many=True)
        return Response({'Jobs': jobs.data})


class getJobsCategory(APIView):
    def get(self, request, *args, **kwargs):
        Name = self.kwargs.get('Category')
        jobs = Job.objects.filter(Classification=Name)
        jobs = JobSerializer(jobs, many=True)
        return Response({'Jobs': jobs.data})
