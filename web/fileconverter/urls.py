from django.urls import path
from .views import ConvertedModelListCreateView, ConvertedModelDetailView

urlpatterns = [
    path('', ConvertedModelListCreateView.as_view(), name='model-list-create'),
    path('<int:pk>/', ConvertedModelDetailView.as_view(), name='model-detail'),
]
