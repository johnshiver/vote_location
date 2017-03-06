
from django.contrib.gis.geos import Point
from rest_framework import generics, exceptions

from .models import District, DistrictDetail
from .serializers import DistrictDetailSerializer


class GetDistrictView(generics.RetrieveAPIView):

    serializer_class = DistrictDetailSerializer


    def get_object(self):

        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')

        if not lat and lon:
            raise exceptions.ParseError()

        try:
            lat, lon = float(lat), float(lon)
        except Exception:
            raise exceptions.ParseError()

        user_point = Point(lon, lat)
        try:
            district = District.objects.get(geom__contains=user_point)
        except District.DoesNotExist:
            raise exceptions.NotFound()
        else:
            return DistrictDetail.objects.get(district_shape=district)


