from django.urls import path
from rest_framework import routers
# from .api import VacancyViewSet

from . import views
# router = routers.DefaultRouter()
# router.register('api/vacancy', VacancyViewSet, 'vacancy')

# urlpatterns = router.urls

urlpatterns = [
    path('vacancy/', views.VacancyListView.as_view()),
    path('vacancy/<int:pk>', views.VacancyDetailView.as_view()),
    path('vacancy/create', views.VacancyCreateView.as_view())
]
