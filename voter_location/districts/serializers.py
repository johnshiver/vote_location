from rest_framework import serializers

from .models import District, DistrictDetail


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ('statename', 'district')


class DistrictDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = DistrictDetail
        fields = ('current_population', 'registered_voters', 'politician_name',
                  'politician_image_url')

    def to_representation(self, value):
        cur_serial = super(DistrictDetailSerializer, self).to_representation(value)
        serialized_district = DistrictSerializer(self.instance.district_shape)
        cur_serial['district_shape'] = serialized_district.data
        cur_serial['politician_url'] = self.instance.politician_ballotpedia_url
        return cur_serial

