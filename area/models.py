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


class Parkingzone(models.Model):
    class Meta:
        db_table = 'parkingzones'

    center_lat = models.DecimalField(max_digits=17, decimal_places=14)
    center_lng = models.DecimalField(max_digits=17, decimal_places=14)
    radius     = models.FloatField()


class ForbiddenArea(models.Model):
    class Meta:
        db_table = 'forbidden_areas'

    boundary = models.PolygonField()
    coords   = models.MultiPointField()
