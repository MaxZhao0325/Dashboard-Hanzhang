from django.db import models

# Create your models here.
class EmaStoringData(models.Model):
    time = models.DateTimeField()
    event_vct = models.CharField(max_length=100, blank=True, null=True)
    stats_vct = models.CharField(max_length=100, blank=True, null=True)
    action = models.IntegerField(blank=True, null=True)
    reward = models.FloatField(blank=True, null=True)
    action_vct = models.CharField(max_length=100, blank=True, null=True)
    message_name = models.CharField(max_length=100, blank=True, null=True)
    uploaded = models.IntegerField(blank=True, null=True)
    dep_id = models.IntegerField()
    p_key = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'ema_storing_data'