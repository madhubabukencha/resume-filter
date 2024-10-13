from django.urls import path
from .views import  (DocumentUploadView, 
                     DocumentListView, 
                     DocumentDeleteView,
                     ExtractedEntitiesListView,
                     download_filtered_data)


urlpatterns = [
    path("", DocumentUploadView.as_view(), name="resume-filter-home"),
    path("uploaded-docs/", DocumentListView.as_view(), name="uploaded-docs"),
    path('delete/<int:pk>/', DocumentDeleteView.as_view(), name='document-delete'),
    path("extracted-entities/", ExtractedEntitiesListView.as_view(), name="extracted-entities"),
    path("download-filtered-data/", download_filtered_data, name="download_filtered_data"),
]