from django.conf.urls import url, include

API_TITLE = 'Home Automation API'
API_DESCRIPTION = 'A Web API for home automation.'


urlpatterns = [
    url(r'^', include('hauto.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]