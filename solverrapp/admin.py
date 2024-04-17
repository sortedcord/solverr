from django.contrib import admin

# Register your models here.
from .models import Question, Solution, Source

admin.site.register(Question)
admin.site.register(Solution)
admin.site.register(Source)