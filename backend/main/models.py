from django.db import models

CAB_TYPES = (
    ("SUV", "SUV"),
    ("SEDAN", "SEDAN"),
    ("HATCHBACK", "HATCHBACK"),
    ("MINI", "MINI"),
)


class Cab(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=CAB_TYPES)
    location_latitude = models.FloatField(max_length=100, null=True, blank=True)
    location_longitude = models.FloatField(max_length=100, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    start_location = models.CharField(max_length=100, null=True, blank=True)
    end_location = models.CharField(max_length=100, null=True, blank=True)
    is_on_trip = models.BooleanField(default=False)
    trip_start_time = models.DateTimeField(null=True, blank=True)
    trip_end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class SharingCab(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=CAB_TYPES)
    location_latitude = models.FloatField(max_length=100, null=True, blank=True)
    location_longitude = models.FloatField(max_length=100, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    start_location = models.CharField(max_length=100, null=True, blank=True)
    end_location = models.CharField(max_length=100, null=True, blank=True)
    passenger1_pickup_location_latitude = models.CharField(
        max_length=100, null=True, blank=True
    )
    passenger1_pickup_location_longitude = models.CharField(
        max_length=100, null=True, blank=True
    )
    passenger1_drop_location_latitude = models.CharField(
        max_length=100, null=True, blank=True
    )
    passenger1_drop_location_longitude = models.CharField(
        max_length=100, null=True, blank=True
    )
    is_on_trip = models.BooleanField(default=False)
    is_empty = models.BooleanField(default=True)
    is_filled = models.BooleanField(default=False)
    trip_start_time = models.DateTimeField(null=True, blank=True)
    trip_end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Driver(models.Model):
    name = models.CharField(max_length=100)
    cab = models.ForeignKey(Cab, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Trip(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    cab = models.ForeignKey(Cab, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    start_location_latitude = models.CharField(max_length=100)
    start_location_longitude = models.CharField(max_length=100)
    end_location_latitude = models.CharField(max_length=100)
    end_location_longitude = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.cab.name + " - " + self.user.username


class SharingTrip(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    cab = models.ForeignKey(SharingCab, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    start_location_latitude = models.CharField(max_length=100)
    start_location_longitude = models.CharField(max_length=100)
    end_location_latitude = models.CharField(max_length=100)
    end_location_longitude = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.cab.name + " - " + self.user.username
