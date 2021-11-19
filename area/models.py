from django.contrib.gis.db import models


class Area(models.Model):
    class Meta:
        db_table = 'area'

    area_boundary = models.PolygonField()
    area_center = models.PointField()
    area_coords = models.MultiPointField()
    basic_fee = models.IntegerField()
    fee_per_min = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
