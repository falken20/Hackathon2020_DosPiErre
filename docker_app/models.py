from django.db import models
import requests

# Create your models here.
API_KEY = ''


class UserItem(models.Model):
    """ Class for saving the different teenagers """
    user = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=10, default='')
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=60, default='', blank=True, null=True)
    age = models.IntegerField()
    address = models.CharField(max_length=60)
    zip_code = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=40)
    province = models.CharField(max_length=40)
    points = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default='0')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default='0')

    def __str__(self):
        return f'{self.name} ({self.user}), Points: {self.points}'

    def save(self, **kwargs):
        geo_address = " ".join([self.address, str(self.zip_code), self.city])
        api_key = API_KEY
        api_response = \
            requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address="{geo_address}"&key={api_key}')
        api_response_dict = api_response.json()
        print(api_response_dict)

        if api_response_dict['status'] == 'OK':
            self.latitude = api_response_dict['results'][0]['geometry']['location']['lat']
            self.longitude = api_response_dict['results'][0]['geometry']['location']['lng']
            self.save()

        super().save(**kwargs)


class CompanyItem(models.Model):
    """ Class para almacenar datos de compañias que ofrecen promocion """
    SECTOR = (
        ('O', 'Ocio'),
        ('T', 'Tiendas'),
        ('R', 'Restaruración'),
        ('I', 'Internet'),
    )
    id_company = models.CharField(max_length=10, primary_key=True)
    company = models.CharField(max_length=60)
    logo_url = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=60)
    zip_code = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=40)
    province = models.CharField(max_length=40)
    sector = models.CharField(max_length=1, choices=SECTOR)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default='0')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default='0')

    def __str__(self):
        return f'{self.company}'

    def save(self, **kwargs):
        geo_address = " ".join([self.address, str(self.zip_code), self.city])
        api_key = API_KEY
        api_response = \
            requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address="{geo_address}"&key={api_key}')
        api_response_dict = api_response.json()
        print(api_response_dict)

        if api_response_dict['status'] == 'OK':
            self.latitude = api_response_dict['results'][0]['geometry']['location']['lat']
            self.longitude = api_response_dict['results'][0]['geometry']['location']['lng']
            self.save()

        super().save(**kwargs)


class QuestionItem(models.Model):
    """ Class para almacenar las preguntas que iran en cada reto"""
    id_question = models.CharField(max_length=10, primary_key=True)
    desc_question = models.TextField(max_length=150)

    def __str__(self):
        return f'{self.desc_question}'


class AnswerItem(models.Model):
    """ Class para almacenar las posibles respuestas a una pregunta """
    id_answer = models.CharField(max_length=10, primary_key=True)
    question = models.ForeignKey(QuestionItem, on_delete=models.CASCADE)
    desc_answer = models.CharField(max_length=50)
    is_ok = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.desc_answer} . Correct: {self.is_ok}'


class RetoItem(models.Model):
    """ Class para los retos que se ofreceran, cada reto puede tener 5 preguntas """
    id_reto = models.CharField(max_length=10, primary_key=True)
    desc_reto = models.CharField(max_length=100)
    questions = models.ManyToManyField(QuestionItem)
    points_1 = models.IntegerField(default=50)
    points_2 = models.IntegerField(default=25)
    points_3 = models.IntegerField(default=10)

    def __str__(self):
        return f'{self.desc_reto}, Points: {self.points_1}, {self.points_2}, {self.points_3}'


class PromotionItem(models.Model):
    """ Class for saving the types of promotions """
    PROMOTION_TYPE = (
        ('D', 'Discount'),
        ('M', 'Merchandising'),
        ('T', 'Free tickets'),
        ('R', 'Regalo'),
    )
    id_promotion = models.CharField(max_length=10, primary_key=True)
    type = models.CharField(max_length=1, choices=PROMOTION_TYPE)
    desc_promotion = models.TextField(max_length=60)
    company = models.ForeignKey(CompanyItem, on_delete=models.PROTECT)
    reto = models.ForeignKey(RetoItem, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.desc_promotion}, Company: {self.company} Tipo: {self.type}'

