from django.contrib.auth.models import User
from django.db import models


class Deer(models.Model):
    class Meta:
        db_table = 'deer'

    area = models.ForeignKey(
        'area.Area',
        on_delete=models.SET_NULL,
        related_name='deers',
        null=True,
    )
    name = models.CharField(max_length=20, unique=True)
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
    deer = models.ForeignKey(
        'vehicle.Deer',
        on_delete=models.SET_NULL,
        related_name='boarding_logs',
        null=True
    )
    use_end_lat = models.DecimalField(
        max_digits=17,
        decimal_places=14,
        null=True
    )
    use_end_lng = models.DecimalField(
        max_digits=17,
        decimal_places=14,
        null=True
    )
    use_start_at = models.DateTimeField()
    use_end_at = models.DateTimeField(null=True)
    in_use = models.BooleanField()
    fee = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

