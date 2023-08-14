from django.db import models
from apps.user.models import User

# Create your models here.
class BusStop(models.Model):
    name = models.CharField(max_length=255)
    distance_from_college = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        """Return the name as string value ."""
        return self.name

    class Meta:
        """Overiding the table name."""

        db_table = 'bus_stop'
        

class Bus(models.Model):
    bus_number = models.CharField(max_length=255)
    destination = models.ForeignKey(BusStop, on_delete=models.RESTRICT, related_name="destination")
    bus_stops = models.ManyToManyField(BusStop)

    def __str__(self):
        """Return the name as string value ."""
        return self.bus_number

    class Meta:
        """Overiding the table name."""

        db_table = 'bus'


class UserBusPass(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    bus = models.ForeignKey(Bus, on_delete=models.RESTRICT)
    boarding_point = models.ForeignKey(BusStop, on_delete=models.RESTRICT)
    created_at = models.DateField()
    expire_at = models.DateField()
    fare = models.IntegerField()
    active = models.BooleanField()

    def __str__(self):
        """Return the name as string value ."""
        return self.user.email

    class Meta:
        """Overiding the table name."""

        db_table = 'user_bus_pass'


class Notification(models.Model):
    notification = models.CharField(max_length=1000)
    seen_by = models.ManyToManyField(User, blank=True)

    def __str__(self):
        """Return the name as string value ."""
        return self.notification

    class Meta:
        """Overiding the table name."""

        db_table = 'notification'