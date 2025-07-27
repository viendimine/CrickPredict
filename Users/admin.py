from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Contest, Question, UserAnswer

admin.site.register(Contest)
admin.site.register(Question)
admin.site.register(UserAnswer)
