from django.db import models


class WarehouseItem(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.title
