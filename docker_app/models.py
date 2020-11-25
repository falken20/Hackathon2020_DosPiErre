from django.db import models

# Create your models here.


class BoyItem(models.Model):
    """ Class for saving the different teenagers """
    user = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=10, default='')
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=60, default='', blank=True, null=True)
    age = models.IntegerField()
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=40)
    province = models.CharField(max_length=40)
    points = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.surname}'


class CompanyItem(models.Model):
    """ Class for saving companies data"""
    id_company = models.CharField(max_length=10, primary_key=True)
    company = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    sector = models.CharField(max_length=20)

"""
class PromotionItem(models.Model):
    # Class for saving the types of promotions
    PROMOTION_TYPE = (
        ('T', 'Ticket discount'),
        ('M', 'Merchandising'),
        ('F', 'Free tickets'),
    )
    type = models.CharField(max_length=1, choices=PROMOTION_TYPE)
    id_company = models.CharField(max_length=10)
    value = models.TextField(60)
    points
"""