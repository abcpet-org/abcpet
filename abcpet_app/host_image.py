from django.db import models

class HostImage(models.Model):
    image = models.ImageField(upload_to='host_images')

    def __str__(self):
        return self.image.name