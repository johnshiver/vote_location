from django.conf.urls import url


from . import api


urlpatterns = [
    url(r'district/$', api.GetDistrictView.as_view()),
]

