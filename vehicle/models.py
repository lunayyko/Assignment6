from django.contrib.auth.models import User
from django.db import models


class EKScooter(models.Model):
    class Meta:
        db_table = 'ek_scooter'

    area = models.ForeignKey(
        'area.Area',
        on_delete=models.SET_NULL,
        related_name='ek_scooters',
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BoardingLog(models.Model):
    class Meta:
        db_table = 'boarding_log'

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='boarding_logs',
        null=True
    )
    ek_scooter = models.ForeignKey(
        'vehicle.EKScooter',
        on_delete=models.SET_NULL,
        related_name='boarding_logs',
        null=True
    )
    use_end_lat = models.DecimalField(max_digits=17, decimal_places=14)
    use_end_lng = models.DecimalField(max_digits=17, decimal_places=14)
    use_start_at = models.DateTimeField()
    use_end_at = models.DateTimeField()
    in_use = models.BooleanField()
    fee = models.IntegerField()
