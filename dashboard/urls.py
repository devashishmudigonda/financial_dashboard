from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views
from .views import FinancialDataViewSet, insights_view

router = DefaultRouter()
router.register(r'financial-data', FinancialDataViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('run-script/', views.run_import_script, name='run_import_script'),
    path('api/', include(router.urls)),  # Ensure this line is included
    path('insights/', insights_view, name='insights'),
]