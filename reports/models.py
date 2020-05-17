from django.db import models

# Create your models here.

class AssociateBill(models.Model):
    id = models.AutoField(primary_key = True)
    bill1 = models.CharField(max_length = 100)
    bill2 = models.CharField(max_length = 200)


    def __srt__(self):
        return self.id
