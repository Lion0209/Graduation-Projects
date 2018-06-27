from django.contrib import admin

# Register your models here.
from repository import models
admin.site.register(models.UserProfile)
admin.site.register(models.UserInfo)
admin.site.register(models.NewsInfo)
admin.site.register(models.NoticeInfo)
admin.site.register(models.AdministratorInfo)
admin.site.register(models.CompetitionInfo)