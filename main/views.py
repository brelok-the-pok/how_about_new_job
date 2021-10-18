import datetime
import json
from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import VacancySerializer

from .models import Vacancy
from rest_framework.views import APIView


class VacancyListView(APIView):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        serializer = VacancySerializer(vacancies, many=True)
        return Response(serializer.data)


class VacancyDetailView(APIView):
    def get(self, request, pk):
        vacancy = Vacancy.objects.get(id=pk)
        serializer = VacancySerializer(vacancy)
        return Response(serializer.data)


class VacancyCreateView(APIView):
    def post(self, request):
        many = isinstance(request.data, list)
        serializer = VacancySerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)
