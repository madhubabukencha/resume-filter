from django.urls import path
from .views import  (DocumentUploadView, 
                     DocumentListView, 
                     DocumentDeleteView)


urlpatterns = [
    path("", DocumentUploadView.as_view(), name="resume-filter-home"),
    path("uploaded-docs/", DocumentListView.as_view(), name="uploaded-docs"),
    path('delete/<int:pk>/', DocumentDeleteView.as_view(), name='document-delete'),
]