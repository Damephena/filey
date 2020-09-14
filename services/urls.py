from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

import services.views as view

router = DefaultRouter()
router.register('upload', view.ItemViewset, basename='upload')

urlpatterns = [
    path('download/<str:pk>/', view.DownloadView.as_view()),
] + router.urls
