from .models import District, DistrictDetail


all_districts = District.objects.all()
for district in all_districts:
    try:
        DistrictDetail.objects.create(district_shape=district)
    except Exception as e:
        print("There was an error creating DistrictDetail: {}".format(e))

