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
