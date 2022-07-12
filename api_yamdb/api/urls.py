from django.urls import include, path
from rest_framework import routers

v1 = routers.DefaultRouter()


urlpatterns = [
    path('v1/', include(v1.urls))
]
