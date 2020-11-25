from django.db import models

# Create your models here.


class UserItem(models.Model):
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
        return f'{self.name} ({self.user})'


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
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=40)
    province = models.CharField(max_length=40)
    sector = models.CharField(max_length=1, choices=SECTOR)

    def __str__(self):
        return f'{self.company}'


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

    def __str__(self):
        return f'{self.desc_reto}'


class PromotionItem(models.Model):
    """ Class for saving the types of promotions """
    PROMOTION_TYPE = (
        ('D', 'Discount'),
        ('M', 'Merchandising'),
        ('T', 'Free tickets'),
    )
    id_promotion = models.CharField(max_length=10, primary_key=True)
    type = models.CharField(max_length=1, choices=PROMOTION_TYPE)
    desc_promotion = models.TextField(60)
    id_company = models.ForeignKey(CompanyItem, on_delete=models.PROTECT)
    reto = models.ForeignKey(RetoItem, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.desc_promotion}'

