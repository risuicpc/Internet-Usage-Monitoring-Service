from django.urls import path
from .views import *

urlpatterns = [
    path('load/data/', LoadData.as_view(), name='load'),
    path('analytics/', AnalyticsAPIView.as_view(), name='analytics'),
    path('user/search/', UserSearchAPIView.as_view(), name='search')
]
