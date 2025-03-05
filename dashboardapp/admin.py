from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Course)
admin.site.register(models.Lesson)
admin.site.register(models.Comment)
admin.site.register(models.Enrollment)