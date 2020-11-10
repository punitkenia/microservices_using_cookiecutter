from django.urls import path

from . import views

urlpatterns = [
    path('bulk_email_api/', views.BulkEmailApi.as_view(), name='bulk-email-api'),
]