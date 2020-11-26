from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.UserItem)
admin.site.register(models.CompanyItem)
admin.site.register(models.QuestionItem)
admin.site.register(models.AnswerItem)
admin.site.register(models.RetoItem)
admin.site.register(models.PromotionItem)
admin.site.register(models.TopicItem)